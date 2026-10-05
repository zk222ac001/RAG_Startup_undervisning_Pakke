# 🟦 Opgave 1 · Forstå og afprøv RAG

[← Opgaveoversigt](README.md) · [Rapportskabelon](rapportskabelon.md)

**Tid:** 2 × 90 minutter efter installation. **Formål:** forstå, hvordan projektet finder tekst og bruger den til et svar.

## Del 1 · Få demoen til at køre · 20 minutter

Følg [opsætningen](../docs/setup.md), og start `rag_demo.py`. Brug de oprindelige filer i `data/` og standardindstillingerne: `size=100`, `overlap=20`, `top_k=2`.

1. Kør `ollama list`, og notér de installerede modelnavne.
2. Stil spørgsmålet `When must I submit the final report?`.
3. Gem de viste tekststykker under `RETRIEVED EVIDENCE` og hele svaret under `ANSWER`.
4. Stil spørgsmålet `What is the Wi-Fi password?`, og gem resultatet.
5. Afslut med `exit`.

**Besvar:** Hvilket dokument indeholder fristen? Indeholder noget dokument Wi-Fi-koden? Hvad gjorde modellen faktisk, da oplysningen manglede?

> [!NOTE]
> Det er ikke en fejl i jeres aflevering, hvis modellen opfinder et svar. Det er en observation, I skal dokumentere og forklare.

**Kontrolpunkt:** I har to spørgsmål med kopieret evidens, faktiske svar og jeres vurdering.

## Del 2 · Følg data gennem programmet · 30 minutter

Læs [kodegennemgangen](../docs/rag-explained.md) og find funktionerne i [rag_demo.py](../rag_demo.py).

| Funktion | Jeres opgave |
| :--- | :--- |
| `load_chunks()` | Forklar, hvor filerne findes, og hvordan kildeetiketter dannes |
| `chunk_text()` | Forklar `split()`, udsnittet og `size - overlap` |
| `embed()` | Forklar, hvad modellen modtager og returnerer |
| `cosine()` | Forklar, hvad funktionen sammenligner |
| `retrieve()` | Forklar sorteringen og valget af de bedste kandidater |
| `answer()` | Find systembeskeden, spørgsmålet og dokumentkonteksten |
| `main()` | Markér, hvad der sker én gang, og hvad der gentages |

Besvar også:

1. Hvorfor har projektet både en embeddingmodel og en chatmodel?
2. Hvorfor bruges samme embeddingmodel til dokumenter og spørgsmål?
3. Hvorfor betyder en lighedsscore på `0.8` ikke “80 % sikkert korrekt”?
4. Bliver modellen trænet på ny, når I tilføjer en tekstfil?
5. Hvorfor kontrollerer koden antallet af vektorer, før den bruger `zip()`?

**Kontrolpunkt:** Lav en skitse eller et diagram med indeksering og spørgsmålsbehandling, og forklar det til en anden gruppe.

## Del 3 · Undersøg chunking uden modelkald · 30 minutter

Opret en midlertidig fil `chunk_forsog.py` i samme mappe som `rag_demo.py`. Importér `chunk_text` fra `rag_demo`, og brug teksten:

```text
Robotten bruger Python og finder vej med sensorer i laboratoriet
```

1. Tæl ordene og forudsig resultatet for `size=6`, `overlap=2` på papir.
2. Kald funktionen, og udskriv hvert tekststykke med et nummer.
3. Gentag med `size=6`, `overlap=0`.
4. Sammenlign jeres forudsigelse med det faktiske resultat.
5. Prøv `size=6`, `overlap=6`. Forklar fejlbeskeden og behovet for kontrollen.

**Hint:** `enumerate(chunks, 1)` kan give tekststykkerne numre. Ollama-modellerne behøver ikke køre til denne del, men Python-afhængighederne skal være installeret.

**Kontrolpunkt:** Aflevér jeres lille forsøgsscript, output for de to gyldige indstillinger og en forklaring på den ugyldige indstilling.

## Del 4 · Sammenlign top-k · 40 minutter

Brug de oprindelige dokumenter. Find denne linje i `main()`:

```python
hits = retrieve(question, records, vectors)
```

Til forsøget kan I angive parameteren direkte:

```python
hits = retrieve(question, records, vectors, top_k=1)
```

Kør disse tre spørgsmål med `top_k=1`, derefter `2` og derefter `3`. Genstart efter hver kodeændring. Hold dokumenter, modeller og chunkindstillinger uændrede.

| ID | Spørgsmål |
| :--- | :--- |
| T1 | `When must I submit the final report?` |
| T2 | `Where should I return borrowed equipment?` |
| T3 | `What is the Wi-Fi password?` |

Registrér alle ni kørsler:

| Spørgsmål | Top-k | Fundne etiketter | Nødvendigt faktum fundet? | Svar understøttet / korrekt afvisning? |
| :--- | ---: | :--- | :--- | :--- |
| T1 | 1 | Udfyld | Ja/nej | Udfyld |

**Diskutér:** Giver flere kilder altid et bedre svar? Hvorfor findes der også kandidater til T3? Hvad kan forsøget fortælle, når der kun er tre korte dokumenter?

**Kontrolpunkt:** Ni registrerede resultater og en konklusion på 5–8 linjer. Gendan det oprindelige kald uden eksplicit `top_k`, inden I fortsætter.

## Del 5 · Opdatér et faktum · 30 minutter

1. Tag en kopi af `data/course.txt` uden for `data/`.
2. Find den fiktive rapportfrist og ændr den til **20 December 2026 at 10:00**. Ændr ikke demonstrationsdatoen.
3. Genstart programmet og spørg igen om rapportfristen.
4. Gem den fundne tekst og det faktiske svar.
5. Gendan originalfilen og genstart igen, så senere forsøg bruger de oprindelige data.

**Besvar:** Hvorfor kræver denne demo genstart? Hvad ligger i RAM? Hvorfor var modeltræning ikke nødvendig? Husk, at facit i `evaluation_questions.json` kun passer til de oprindelige dokumenter.

## Aflevering · 30 minutter til opsamling

Aflevér forsøgsnoter i [rapportskabelonen](rapportskabelon.md), jeres diagram og `chunk_forsog.py`. Noterne skal indeholde:

- To startspørgsmål med evidens og svar.
- Forklaringer til kode og begreber.
- Chunking-forsøg med forudsigelser og faktisk output.
- Ni top-k-resultater og en konklusion.
- Dokumentation for ændringen af fristen og efterfølgende gendannelse.

**Klar til opgave 2?** I skal kunne forklare forskellen mellem “den rigtige tekst blev ikke fundet” og “modellen fik teksten, men svarede forkert”.
