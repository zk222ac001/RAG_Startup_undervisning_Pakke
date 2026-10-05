# RAG teaching guide (English)

[Back to README](../README.md) · [Current validation](validation.md)

The original teaching material is preserved below. The Danish guides provide the reorganized walkthrough and current error handling.

RAG TEACHING PACK — BEGINNER PYTHON CLASS

Goal: build a local assistant that retrieves evidence from text files, answers
questions with source labels, and is evaluated on answerable and missing facts.
All supplied course policies are FICTIONAL. Replace them before real use.

## WINDOWS SETUP
1. Install Python 3.11+ and Ollama from https://ollama.com/download.
2. Open Ollama. Open this extracted folder in VS Code, then open a terminal.
3. Run these commands (no environment activation is required):

   py -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ollama pull embeddinggemma
   ollama pull llama3.2:3b
   .venv\Scripts\python.exe rag_demo.py

macOS/Linux: use python3 -m venv .venv, then .venv/bin/python in place of
.venv\Scripts\python.exe. The ollama commands are the same.

Alternative with uv (after installing Ollama and pulling both models):
   uv venv
   uv pip install -r requirements.txt
   uv run --no-project python rag_demo.py

Model downloads require internet, disk space and time. Inference uses your
computer; speed depends on memory and hardware. No paid API key is required.
Run the demo before class on the actual classroom computers.

## WHAT IS RAG?
Retrieval-Augmented Generation means retrieving relevant information and
giving it to a language model as context for its answer. Think of an open-book
exam: first find the useful page, then answer from that page.
This does not train or update the model weights. A basic RAG pipeline is not
necessarily an agent: the steps here are fixed in Python.

## TWO PHASES
Indexing: files -> text -> chunks -> embeddings -> in-memory index.
Question answering: question -> embedding -> similar chunks -> prompt -> answer.
An embedding is a numeric representation useful for comparing text meanings.
The same embedding model must encode the chunks and the question.
The chat model is separate: it writes the final natural-language answer.

## TEACHING ROADMAP: FOUR SESSIONS, EACH 90 MINUTES
Before class: students know functions, lists, dictionaries, loops and file I/O.
Have students download models before the first practical session.

Session 1 — Understand the problem
  0–15: Ask for a private course deadline. Why can't a model reliably know it?
 15–30: Explain RAG and the open-book analogy; distinguish it from training.
 30–50: Run the demo. Inspect retrieved evidence before reading the answer.
 50–75: Groups manually find relevant passages for five questions.
 75–90: Students explain retrieval, context and generation in their own words.
 Outcome: explain how a document becomes evidence for an answer.

Session 2 — Build retrieval
  0–20: Load files; explain chunk_text and overlapping windows.
 20–40: Create embeddings and inspect vector lengths.
 40–60: Explain cosine similarity: compare vector directions, not word counts.
 60–80: Run paraphrased queries; compare top_k=1 and top_k=2.
 80–90: Check whether the needed evidence was retrieved.
 Outcome: retrieve relevant chunks without relying on the generated answer.

Session 3 — Generate grounded answers
  0–20: Build a prompt from the question plus retrieved evidence.
 20–40: Inspect roles, source labels and missing-answer instructions.
 40–60: Ask about facts absent from every file. Record any invented answers.
 60–80: Change a fact in a document, restart, and ask again.
 80–90: Explain why no model retraining was needed.
 Outcome: connect retrieval to generation and recognize limitations.

Session 4 — Evaluate and finish a mini-project
  0–20: Choose a document collection and define its scope.
 20–45: Test with evaluation_questions.json and add domain questions.
 45–65: Diagnose failures: retrieval failure or unsupported generation?
 65–80: Improve chunking/top_k and repeat exactly the same question set.
 80–90: Present evidence, results and limitations.
 Outcome: a working document assistant plus an honest evaluation.

## LIVE DEMO QUESTIONS
1. When must I submit the final report?
   Expected fact: 12 December 2026 at 12:00. Source: course.txt.
2. What time does the robotics lab close?
   Expected fact: 16:00 Monday–Friday. Source: lab.txt.
3. How much of the grade comes from the demonstration?
   Expected fact: 40 percent. Source: assessment.txt.
4. What is the Wi-Fi password?
   Expected behavior: say the documents do not provide it.
Generated wording and ranking can vary. These are expectations, not captured
outputs. A prompt requesting abstention does not guarantee it.

## CODE WALKTHROUGH
load_chunks: reads UTF-8 .txt files beside the script and retains source labels.
chunk_text: splits long text into 100-word windows with 20-word overlap.
  The supplied files are short; each currently fits in one chunk. To demonstrate
  overlap, add a longer text or temporarily use size=30 and overlap=5.
embed: sends text to the local embedding model and receives vectors.
cosine: compares two vector directions. Scores are not probabilities.
retrieve: embeds the question, scores all chunks, selects the two best.
answer: sends question and selected evidence to the local chat model.
main: builds the index once per launch and handles questions repeatedly.

## EXERCISES
A. Add equipment.txt with five invented equipment policies; ask three questions.
B. Paraphrase 'When must I submit the final report?' without using 'report'.
C. Add a 300-word document and compare chunk sizes 30, 60, and 100.
D. Compare top_k=1, 2, and 3. More context is not always more useful.
E. Change the deadline, restart, and verify that the updated text is retrieved.
F. Add a deliberately misleading instruction in a document. Discuss whether
   the model obeys it. Prompt instructions alone are not a security boundary.

## ASSESSMENT / WHERE TO FINISH
Submit: Python code; at least five documents; ten questions (seven answerable,
three unanswerable); expected answers and sources; actual answers; a brief
discussion of two failures and one measured improvement.
Record retrieval hit rate on answerable questions: cases where the expected
source appears among retrieved chunks / number of answerable questions.
Also manually score factual correctness, whether cited evidence really supports
claims, and appropriate abstention on the unanswerable questions.
Suggested classroom targets: evidence found for at least 6/7 answerable cases,
correct supported answers for at least 6/7, and abstention for 3/3 missing facts.
These are classroom targets, not production reliability claims.

## LIMITATIONS AND NEXT STEPS
The index is in RAM and rebuilt on every launch. Editing files requires restart.
Top-k always returns candidates, even for unrelated questions. The model must
recognize missing evidence; this can fail. Do not treat similarity as confidence
or adopt an arbitrary universal similarity cutoff.
Source labels are requested from the model, not independently verified.
This simple word splitter may break sentences and does not count model tokens.
Start with text files. Add PDF parsing/OCR, persistent vector storage, metadata
filters, hybrid search and reranking only after students understand this demo.
For deployment, add document permissions, deletion/update handling, citation
validation and evaluation on realistic questions.

## TROUBLESHOOTING
Connection refused: open Ollama, or run ollama serve in another terminal.
Model missing: run ollama list, then pull the missing model listed above.
ollama command unknown: install Ollama and reopen the terminal.
ModuleNotFoundError: install requirements with the same Python used to run it.
Slow generation/out of memory: try ollama pull llama3.2:1b and change CHAT_MODEL;
this may reduce answer quality. Close other memory-heavy applications.
Unhelpful answers: inspect the printed evidence first, then the prompt.
Long-document errors: reduce chunk size; word count is not token count.

## VALIDATION
Python syntax and a simulated end-to-end retrieval-to-prompt smoke check were
checked during preparation. Real Ollama model inference was not run here.
Confirm real retrieval quality, speed, citations and missing-answer behavior
on your own computer before teaching.

## OFFICIAL REFERENCES (checked 30 September 2026)
https://docs.ollama.com/capabilities/embeddings
https://github.com/ollama/ollama-python
https://ollama.com/library/llama3.2
