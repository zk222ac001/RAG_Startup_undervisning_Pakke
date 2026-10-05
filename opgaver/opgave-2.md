# 🟪 Opgave 2 · Byg din egen dokumentassistent

[← Opgaveoversigt](README.md) · [Rapportskabelon](rapportskabelon.md)

**Tid:** 2 × 90 minutter + 2–3 timers hjemmearbejde. **Forudsætning:** opgave 1. **Formål:** udvide projektet og evaluere, om svarene er understøttet af dokumenterne.

## Case · En assistent til et fiktivt robotlaboratorium

Nye studerende har spørgsmål om udstyr, åbningstider, projektkrav og booking. I skal bygge en assistent, som bruger laboratoriets tekstfiler til at besvare spørgsmål. Den skal også kunne indrømme, når dokumenterne ikke indeholder svaret.

I må vælge en tilsvarende case, fx en fiktiv kursus-FAQ, hvis kravene nedenfor stadig opfyldes.

> [!IMPORTANT]
> I bygger videre på `rag_demo.py` og bruger lokale Ollama-modeller. En webapp, PDF-læser eller vektordatabase er ikke et krav. Fokus er forståelse, evidens og evaluering.

## Del 1 · Afgræns viden og skriv dokumenter

Skriv 5–8 linjer om målgruppen, hvad assistenten må svare på, og hvad den ikke kan vide.

Opret **mindst fem UTF-8 `.txt`-filer** direkte i `data/`. I kan beholde de tre medfølgende filer og tilføje fx `equipment.txt` og `booking.txt` eller erstatte samlingen med egne fiktive dokumenter. Placér sikkerhedskopier uden for `data/`.

Krav til dokumenterne:

- Hver fil har et tydeligt emne og mindst tre konkrete oplysninger.
- Mindst én fil indeholder **300–400 meningsfulde ord**, så chunking kan undersøges.
- Oplysningerne er indbyrdes konsistente og tydeligt mærket som fiktive.
- I kan pege på præcis den sætning, som understøtter hvert forventet svar.

**Kontrolpunkt:** Alle dokumenter læses, og den lange fil giver flere chunks. Forklar, hvorfor meget korte dokumenter ikke er nok til at undersøge chunkgrænser.

## Del 2 · Tilpas og forklar programmet

Bevar kildeetiketter, evidensvisning og instruktionen om at afvise spørgsmål uden svargrundlag. Tilføj:

1. En velkomsttekst, der fortæller brugeren, hvilket emne assistenten dækker.
2. En kort besked om dokumenternes begrænsninger og stopkommandoen.
3. En visning af antal indlæste dokumenter og antal chunks ved opstart. Tæl unikke kildefiler, ikke hvert chunk som et nyt dokument.
4. Danske kommentarer til jeres ændringer.

**Kontrolpunkt:** Et skærmbillede eller terminaludskrift viser velkomsten og korrekte antal. Hvert gruppemedlem skal kunne forklare én kodeændring.

## Del 3 · Lav et fast evalueringssæt

Opret `evaluation_questions_project.json` i projektets rod med **præcis ti spørgsmål**:

| Type | Antal | Krav |
| :--- | ---: | :--- |
| Besvarlige spørgsmål | 7 | Fordelt over mindst fire kildefiler; mindst to spørgsmål bruger andre formuleringer end dokumenterne |
| Spørgsmål uden svar | 3 | Svaret findes ikke i nogen af jeres dokumenter |

Brug felterne `question`, `expected` og `source` som i [det eksisterende evalueringssæt](../evaluation_questions.json). Brug `null` som kilde ved ubesvarlige spørgsmål. Hvert besvarligt spørgsmål skal kunne besvares fra én angivet kildefil, så målingen er entydig.

**Formateksempel — kun gyldigt, hvis jeres dokument faktisk indeholder reglen:**

```json
[
  {
    "question": "How long may I reserve the test track?",
    "expected": "30 minutes",
    "source": "booking.txt"
  },
  {
    "question": "What is the laboratory Wi-Fi password?",
    "expected": "Abstain: not supplied",
    "source": null
  }
]
```

Lad en anden gruppe kontrollere jeres facit og manglende oplysninger. Fastlås derefter spørgsmålene, før I måler.

> [!NOTE]
> JSON-filen er et facit til manuel evaluering. Den eksisterende demo læser den ikke automatisk. Indtast spørgsmålene i terminalen, og send ikke facit med til modellen.

## Del 4 · Mål et udgangspunkt

Brug `size=100`, `overlap=20` og `top_k=2`. Kør alle ti spørgsmål, og gem for hvert spørgsmål:

- Det fulde spørgsmål og det forventede svar.
- Alle fundne kildeetiketter og de tilhørende tekststykker.
- Det faktiske modelsvar, inklusive eventuelle kildehenvisninger.
- Jeres vurdering med en kort begrundelse.

Beregn tre separate mål:

| Mål | Beregning |
| :--- | :--- |
| Retrieval hit rate | Antal besvarlige spørgsmål, hvor den forventede kildefil findes blandt kandidaterne / 7 |
| Understøttede svar | Antal besvarlige spørgsmål med korrekt svar, understøttende fundet tekst og korrekt kildehenvisning / 7 |
| Korrekte afvisninger | Antal ubesvarlige spørgsmål, hvor modellen tydeligt oplyser, at kilderne ikke indeholder svaret og undlader at gætte / 3 |

Fjern `#chunkN`, når I sammenligner en kildeetiket med `source`. Kontrollér også indholdet: den rigtige fil kan være fundet, selv om det nødvendige faktum ligger i et andet chunk.

## Del 5 · Ændr én indstilling og gentag

Vælg **én** ændring:

| Forsøg | Udgangspunkt → ændring | Hold fast |
| :--- | :--- | :--- |
| A · Chunkstørrelse | `size=100` → `size=60` | `overlap=20`, `top_k=2`, modeller og dokumenter |
| B · Antal kandidater | `top_k=2` → `top_k=3` | `size=100`, `overlap=20`, modeller og dokumenter |

For A ændres standardværdien i `def chunk_text(text, size=100, overlap=20):`. For B angives `top_k=3` i kaldet til `retrieve` inde i `main()`. Se opgave 1 for kaldets placering.

Genstart, kør de **samme ti spørgsmål**, og gem resultaterne igen. Sammenlign de tre mål i en før/efter-tabel.

**Diskutér:** Hvad ændrede sig? Hvorfor? Hvad kan ikke konkluderes ud fra kun ti spørgsmål? En uændret eller dårligere måling er også et gyldigt resultat, hvis den dokumenteres ærligt. Opfind ikke en forbedring; foreslå i stedet et begrundet næste forsøg.

## Del 6 · Analysér fejl og demonstrér løsningen

Vælg to konkrete problematiske eller begrænsende tilfælde. Forklar for hvert:

1. Hvad forventede I, og hvad skete der?
2. Manglede oplysningen i dokumenterne, blev det forkerte chunk fundet, eller brugte modellen evidensen forkert?
3. Hvilken ændring ville I prøve, og hvordan ville I måle virkningen?

Hvis alle svar lykkedes, tilføj to ekstra udfordrende spørgsmål til en separat analyse. Bland dem ikke ind i før/efter-målingens ti spørgsmål. Et spørgsmål uden dokumenteret svar er også relevant til at diskutere systemets afgrænsning.

Forbered en **5-minutters demonstration**: kort case, ét besvarligt spørgsmål, ét ubesvarligt spørgsmål og jeres vigtigste før/efter-resultat.

## 📦 Aflevering

Aflevér et Git-repository eller en ZIP med:

- Den tilpassede `rag_demo.py` og nødvendige afhængigheder.
- Mindst fem `.txt`-dokumenter og `evaluation_questions_project.json`.
- To gemte kodeversioner eller Git-commits, så begge forsøgsindstillinger kan genskabes.
- Udfyldt [rapportskabelon](rapportskabelon.md), normalt 3–5 sider plus resultater som bilag.
- Alle 20 evalueringsresultater: ti før og ti efter, med evidens og faktiske svar.
- En kort kørselsvejledning, gruppemedlemmernes bidrag og beskrivelse af eventuel AI-hjælp.

Medtag ikke `.venv`, modeldownloads, adgangsnøgler eller personfølsomme data.

## ✅ Forslag til bedømmelseskriterier

| Område | Vægt | Tegn på en god aflevering |
| :--- | ---: | :--- |
| Faglig forståelse | 25 % | Forklarer begge RAG-faser, modeller og begrænsninger korrekt |
| Program og dokumenter | 25 % | Løsningen kan startes; ændringer kan forklares; dokumentkrav er opfyldt |
| Evaluering | 30 % | Fast facit, alle 20 resultater og korrekt beregnede mål |
| Analyse og formidling | 20 % | Evidensbaseret før/efter-analyse, to konkrete tilfælde og tydelig demo |

> [!TIP]
> I vurderes på jeres forståelse og dokumentation. En høj modelscore alene er ikke nok, og en dokumenteret modelfejl er ikke det samme som en dårligt løst opgave.

## ⭐ Frivillig ekstraopgave

Lav et separat Python-script, der læser jeres ti spørgsmål, kalder projektets funktioner og gemmer spørgsmål, kilder, tekststykker og svar i JSON. Facit må ikke sendes til modellen. Lad stadig et menneske vurdere, om kilderne understøtter svarene.
