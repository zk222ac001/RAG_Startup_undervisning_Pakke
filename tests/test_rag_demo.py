"""Offline regression tests; model calls are mocked, not evaluated."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import httpx
import ollama
import rag_demo as rag


class RagTests(unittest.TestCase):
    def test_chunk_overlap_and_final_window(self):
        self.assertEqual(rag.chunk_text('a b c d e f g h i j', 6, 2),
                         ['a b c d e f', 'e f g h i j'])
        self.assertEqual(rag.chunk_text('a b c d e f g', 6, 2),
                         ['a b c d e f', 'e f g'])
        self.assertEqual(rag.chunk_text('   '), [])

    def test_invalid_chunk_settings(self):
        for size, overlap in [(0, 0), (2, 2), (2, -1), (2.5, 1), (True, 0)]:
            with self.subTest(size=size, overlap=overlap), self.assertRaises(ValueError):
                rag.chunk_text('abc', size, overlap)

    def test_load_sorted_files_bom_and_ignore_other_formats(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'b.txt').write_text('Hej æøå', encoding='utf-8-sig')
            (root / 'a.txt').write_text('First', encoding='utf-8')
            (root / 'empty.txt').write_text('  ', encoding='utf-8')
            (root / 'ignore.md').write_text('Ignore', encoding='utf-8')
            records = rag.load_chunks(root)
            self.assertEqual([r['source'] for r in records], ['a.txt#chunk1', 'b.txt#chunk1'])
            self.assertEqual(records[1]['text'], 'Hej æøå')

    def test_empty_and_missing_data(self):
        with tempfile.TemporaryDirectory() as folder:
            for path in [Path(folder), Path(folder) / 'missing']:
                with self.subTest(path=path), self.assertRaises(ValueError):
                    rag.load_chunks(path)

    def test_cosine_geometry(self):
        self.assertAlmostEqual(rag.cosine([1, 0], [2, 0]), 1)
        self.assertAlmostEqual(rag.cosine([1, 0], [0, 1]), 0)
        self.assertAlmostEqual(rag.cosine([1, 0], [-1, 0]), -1)
        self.assertEqual(rag.cosine([0, 0], [1, 0]), 0)
        with self.assertRaises(ValueError):
            rag.cosine([1], [1, 2])

    def test_malformed_embeddings(self):
        for vectors, count in [([], 1), ([[]], 1), ([[1], [1, 2]], 2),
                               ([[float('nan')]], 1), ([[float('inf')]], 1), ([[0, 0]], 1)]:
            with self.subTest(vectors=vectors), self.assertRaises(ValueError):
                rag.validate_vectors(vectors, count)

    def test_embed_disables_silent_truncation(self):
        with patch.object(rag.CLIENT, 'embed', return_value={'embeddings': [[1, 0]]}) as call:
            self.assertEqual(rag.embed(['text']), [[1, 0]])
            self.assertFalse(call.call_args.kwargs['truncate'])
            self.assertEqual(rag.embed([]), [])
            call.assert_called_once()

    def test_retrieval_ranking_and_top_k(self):
        records = [{'source': 'low'}, {'source': 'high'}, {'source': 'middle'}]
        with patch.object(rag, 'embed', return_value=[[1, 0]]):
            hits = rag.retrieve('question', records, [[-1, 0], [1, 0], [0, 1]], 2)
            self.assertEqual([r['source'] for r, _ in hits], ['high', 'middle'])
            self.assertEqual(len(rag.retrieve('q', records, [[1, 0]] * 3, 99)), 3)

    def test_retrieval_rejects_invalid_inputs_before_model_call(self):
        with patch.object(rag, 'embed') as call:
            for question, records, vectors, k in [('q', [{}], [], 2), ('q', [], [], 2),
                                                   (' ', [{}], [[1]], 2), ('q', [{}], [[1]], 0),
                                                   ('q', [{}], [[1]], -1), ('q', [{}], [[1]], 1.5)]:
                with self.subTest(k=k, question=question), self.assertRaises(ValueError):
                    rag.retrieve(question, records, vectors, k)
            call.assert_not_called()

    def test_query_dimension_mismatch(self):
        with patch.object(rag, 'embed', return_value=[[1, 0]]), self.assertRaises(ValueError):
            rag.retrieve('q', [{}], [[1]])

    def test_answer_without_evidence_does_not_call_model(self):
        with patch.object(rag.CLIENT, 'chat') as call:
            self.assertEqual(rag.answer('q', []), rag.UNKNOWN)
            call.assert_not_called()

    def test_answer_preserves_evidence_and_guardrails(self):
        with patch.object(rag.CLIENT, 'chat', return_value={'message': {'content': 'Answer'}}) as call:
            self.assertEqual(rag.answer('When?', [({'source': 'a.txt#chunk1', 'text': 'On Friday'}, .9)]), 'Answer')
            messages = call.call_args.kwargs['messages']
            self.assertIn('[a.txt#chunk1]\nOn Friday', messages[1]['content'])
            self.assertIn('untrusted data', messages[0]['content'])
            self.assertIn(rag.UNKNOWN, messages[0]['content'])

    def test_empty_model_answer(self):
        with patch.object(rag.CLIENT, 'chat', return_value={'message': {'content': '  '}}), self.assertRaises(ValueError):
            rag.answer('q', [({'source': 'a', 'text': 'b'}, 1)])

    def test_main_smoke_and_blank_input(self):
        with patch.object(rag, 'load_chunks', return_value=[{'source': 'a#chunk1', 'text': 'Evidence'}]), \
             patch.object(rag.CLIENT, 'embed', return_value={'embeddings': [[1, 0]]}) as embed, \
             patch.object(rag.CLIENT, 'chat', return_value={'message': {'content': 'Supported [a#chunk1]'}}) as chat, \
             patch('builtins.input', side_effect=[' ', 'Question', 'EXIT']), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(rag.run(), 0)
            self.assertEqual(embed.call_count, 2)
            chat.assert_called_once()
            self.assertIn('RETRIEVED EVIDENCE', output.getvalue())
            self.assertIn('Supported [a#chunk1]', output.getvalue())

    def test_actionable_failure_messages_and_exit_status(self):
        cases = [(ConnectionError(), 'Cannot connect'), (httpx.ConnectError('refused'), 'Cannot connect'),
                 (httpx.ReadTimeout('slow'), 'timed out'), (ollama.ResponseError('missing', 404), 'Required models'),
                 (ValueError('bad data'), 'configuration error'), (OSError('unreadable'), 'configuration error'),
                 (UnicodeError('bad encoding'), 'configuration error'),
                 (httpx.RemoteProtocolError('broken'), 'request failed')]
        for error, message in cases:
            with self.subTest(error=error), patch.object(rag, 'main', side_effect=error), \
                 contextlib.redirect_stderr(io.StringIO()) as output:
                self.assertEqual(rag.run(), 1)
                self.assertIn(message, output.getvalue())

    def test_user_stop_is_successful(self):
        for error in [EOFError(), KeyboardInterrupt()]:
            with patch.object(rag, 'main', side_effect=error), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(rag.run(), 0)

    def test_evaluation_sources_exist(self):
        questions = json.loads((rag.DATA.parent / 'evaluation_questions.json').read_text())
        self.assertEqual(sum(q['source'] is not None for q in questions), 7)
        self.assertEqual(sum(q['source'] is None for q in questions), 3)
        for q in questions:
            if q['source']:
                self.assertTrue((rag.DATA / q['source']).is_file())


if __name__ == '__main__':
    unittest.main()
