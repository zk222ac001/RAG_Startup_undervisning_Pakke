# 📝 Rapport · Lokal RAG-assistent

[← Opgaveoversigt](README.md)

Kopiér filen til jeres egen aflevering, og erstat vejledningsteksten med jeres observationer. Gem længere udskrifter i et bilag uden for `data/`.

## 1 · Gruppe og forsøgsopsætning

| Felt | Udfyld |
| :--- | :--- |
| Navne og dato | … |
| Case og målgruppe | … |
| Computer og operativsystem | … |
| Python- og Ollama-version | … |
| Embeddingmodel og chatmodel | … |
| Model-ID fra `ollama list` | … |
| Dokumenter og deres version | … |
| Kodeversion/Git-commit før og efter | … |

## 2 · Opgave 1: Forståelse og forsøg

Indsæt jeres RAG-diagram og forklaringer til funktionerne. Besvar de fem begrebsspørgsmål fra opgave 1.

### Første kørsel

Indsæt de to spørgsmål med fundne tekststykker, faktiske svar og jeres vurdering.

### Chunking

| Indstilling | Forudsagt resultat | Faktisk resultat | Forklaring |
| :--- | :--- | :--- | :--- |
| size=6, overlap=2 | … | … | … |
| size=6, overlap=0 | … | … | … |
| size=6, overlap=6 | … | Fejlbesked: … | … |

### Top-k

Udfyld én række for hver af de ni kørsler. Gem fulde svar og evidens i bilaget.

| Spørgsmål | Top-k | Fundne etiketter | Faktum fundet? | Understøttet svar eller korrekt afvisning? | Bilag |
| :--- | ---: | :--- | :--- | :--- | :--- |
| T1 | 1 | … | … | … | … |

**Konklusion:** …

### Ændret frist

Beskriv ændringen, genstarten og resultatet. Bekræft, at originaldata blev gendannet. Forklar, hvorfor dette ikke var modeltræning.

## 3 · Opgave 2: Afgrænsning og implementering

Hvem bruger assistenten? Hvad kan dokumenterne besvare? Hvilke oplysninger mangler bevidst?

| Dokument | Emne | Antal ord | Eksempel på en konkret oplysning |
| :--- | :--- | ---: | :--- |
| … | … | … | … |

Beskriv jeres kodeændringer. Indsæt velkomsttekst samt antal dokumenter og chunks.

## 4 · Fast spørgsmålssæt og facit

Henvis til `evaluation_questions_project.json`. Forklar, hvordan I kontrollerede de syv svar og sikrede, at de tre øvrige oplysninger ikke findes i dokumenterne.

## 5 · Resultater før og efter

| Indstilling | Før | Efter |
| :--- | :--- | :--- |
| Chunkstørrelse | 100 | … |
| Overlap | 20 | … |
| Top-k | 2 | … |
| Antal chunks | … | … |

**Den eneste ændrede forsøgsindstilling:** …

Udfyld ti rækker pr. kørsel. `Ikke relevant` bruges for kilde-hit og understøttet svar ved ubesvarlige spørgsmål og for afvisning ved besvarlige spørgsmål.

| Kørsel | Spørgsmåls-ID | Kilde-hit? | Understøttet svar? | Korrekt afvisning? | Begrundelse og bilag |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Før | Q1 | … | … | Ikke relevant | … |
| Efter | Q1 | … | … | Ikke relevant | … |

| Mål | Før | Efter |
| :--- | :--- | :--- |
| Retrieval hit rate | … / 7 | … / 7 |
| Understøttede svar | … / 7 | … / 7 |
| Korrekte afvisninger | … / 3 | … / 3 |

**Fortolkning:** Forklar virkningen, og om den nødvendige tekst faktisk var i de fundne chunks. Beskriv usikkerhed og begrænsninger ved forsøget.

## 6 · To konkrete tilfælde

Gentag disse punkter for hvert tilfælde:

- Spørgsmål og forventning.
- Fundet evidens og faktisk modelsvar.
- Forklaring på fejl eller begrænsning.
- Forslag til næste ændring og en måling af dens effekt.

## 7 · Konklusion, arbejdsfordeling og AI-hjælp

Hvad lærte I? Hvad kan løsningen bruges til? Hvad kræver mere arbejde? Hvad bidrog hvert gruppemedlem med? Hvilke AI-forslag brugte I, og hvordan blev de kontrolleret?

## Bilag · Faktiske resultater

Kopiér denne blok for hvert spørgsmål og hver kørsel. Der skal være 20 blokke til opgave 2 samt forsøgsresultaterne fra opgave 1.

### Kørsel: før/efter · Spørgsmål: Q…

**Spørgsmål:** …

**Forventet svar og kilde:** …

**Fundne tekststykker med etiketter og scores:**

```text
Indsæt faktisk terminaloutput her.
```

**Faktisk modelsvar:**

```text
Indsæt det fulde svar her.
```

**Vurdering og begrundelse:** …
