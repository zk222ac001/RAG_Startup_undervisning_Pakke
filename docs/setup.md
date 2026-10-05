# 🚀 Opsætning · Din første lokale RAG

[← Tilbage til forsiden](../README.md)

## 1 · Klargør computeren

Installér Python 3.11 eller nyere og [Ollama](https://ollama.com/download). Download og udpak repoet, eller brug Git:

```bash
git clone https://github.com/zk222ac001/RAG_Startup_undervisning_Pakke.git
cd RAG_Startup_undervisning_Pakke
```

Åbn mappen i VS Code. Alle følgende kommandoer køres i mappen med `requirements.txt`. Brug én af de tre installationsmetoder nedenfor.

## 2 · Installér Python-pakker

### Windows · PowerShell eller kommandoprompt

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

### Alternativ · uv

Hvis uv allerede er installeret:

```bash
uv venv --python 3.11
uv pip install -r requirements.txt
```

> [!TIP]
> Aktivering af miljøet er ikke nødvendig. Kommandoerne bruger den præcise Python i `.venv`, så installation og kørsel bruger samme miljø.

## 3 · Download de to modeller

Start Ollama-appen. På systemer uden en kørende Ollama-tjeneste: kør `ollama serve` i en separat terminal. Kør derefter:

```bash
ollama pull embeddinggemma
ollama pull llama3.2:3b
ollama list
```

| Model | Arbejde |
| :--- | :--- |
| `embeddinggemma` | Gør både dokumenter og spørgsmål til vektorer |
| `llama3.2:3b` | Skriver svar ud fra de fundne tekststykker |

Modellerne kræver diskplads og hukommelse; downloadtid og svartid afhænger af din computer. Afprøv på de faktiske undervisningscomputere.

## 4 · Kør demoen

Windows:

```powershell
.venv\Scripts\python.exe rag_demo.py
```

macOS/Linux:

```bash
.venv/bin/python rag_demo.py
```

uv:

```bash
uv run --no-project python rag_demo.py
```

Spørg: `When must I submit the final report?`. Kontrollér at de viste kilder indeholder fristen. Spørg derefter: `What is the Wi-Fi password?`. Modellen bør oplyse, at kilderne ikke indeholder svaret.

## 5 · Tilføj dine egne dokumenter

1. Gem en almindelig `.txt`-fil i `data/` med UTF-8-kodning.
2. Brug korte afsnit med tydelige fakta. Kun `.txt`-filer direkte i mappen læses.
3. Stop og genstart programmet, så indekset bliver genopbygget.
4. Stil et spørgsmål, der kræver oplysninger fra den nye fil.
5. Kontrollér kildeetiketten, fx `[equipment.txt#chunk1]`.

> [!NOTE]
> Dokumentmappen findes relativt til scriptet. Du kan derfor køre scriptet via en absolut sti fra en anden mappe. PDF, Word og undermapper understøttes ikke af denne begynderdemo.

## Justér forsøget

| Indstilling i `rag_demo.py` | Standard | Virkning |
| :--- | :--- | :--- |
| `chunk_text(..., size=100, overlap=20)` | 100 ord / 20 ord | Tekststykkers størrelse og fælles ord |
| `retrieve(..., top_k=2)` | 2 | Antal tekststykker sendt til chatmodellen |
| `CHAT_MODEL` | `llama3.2:3b` | Modellen, der skriver svar |
| `EMBED_MODEL` | `embeddinggemma` | Modellen, der repræsenterer tekst |

Til en mindre chatmodel: kør `ollama pull llama3.2:1b`, ændr `CHAT_MODEL` til `"llama3.2:1b"`, og genstart. Svarenes kvalitet kan ændre sig. Brug altid samme embeddingmodel til dokumenter og spørgsmål.
