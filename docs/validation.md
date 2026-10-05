# ✅ Validering og rettelser

[← Tilbage til forsiden](../README.md)

## Hvad blev rettet?

| Problem | Ændring |
| :--- | :--- |
| Forsiden indeholdt kun et repositorynavn | Ny dansk README med navigation, hurtig start og illustrationer |
| Undervisningsmateriale var samlet i en lang tekstfil | Separate Markdown-guider; den oprindelige engelske tekst er bevaret |
| `zip` kunne skjule forskelligt antal dokumenter og vektorer | Antal og dimensioner valideres før rangering |
| Ugyldig `top_k` kunne give tomme eller uventede resultater | Kræver et positivt heltal; tomme spørgsmål afvises |
| Chunkindstillinger af forkert type gav uklare fejl | Kontrollerer heltal, størrelse og overlap |
| Embeddings kunne indeholde tomme, ikke-endelige eller nulvektorer | Validering af modelsvar med tydelige fejl |
| Ollama kunne afkorte lange embeddinginput uden fejl | `truncate=False` gør problemet synligt |
| Timeout, filfejl og ugyldig UTF-8 gav tracebacks | Handlingsrettede fejlbeskeder og statuskode 1 |
| Windows UTF-8 BOM kunne blive del af teksten | Indlæsning med `utf-8-sig` |
| Tom evidens blev stadig sendt til chatmodellen | Direkte afvisning uden modelkald |
| Tomt modelsvar blev vist uden forklaring | Tydelig fejlbesked |
| Lighed blev beregnet to gange for udvalgte chunks | Én beregning pr. kandidat |
| Ingen automatiske regressionstests | 17 offline-tests og en GitHub Actions-workflow |

## Udførte kontroller

- 17 tests bestået lokalt med Python 3.12, Ollama Python 0.6.3 og HTTPX 0.28.1.
- Simuleret gennemløb fra indlæsning til embeddings, retrieval, prompt og svar.
- Fejlscenarier: manglende data, ugyldige vektorer, forbindelsesfejl, timeout, API-fejl og brugerstop.
- Lokale Markdown-links, SVG-struktur og whitespace kontrolleret.
- Begge SVG-illustrationer renderet og visuelt kontrolleret.

GitHub Actions er konfigureret til Python 3.11, 3.12 og 3.13 på Windows og Ubuntu. En konfigureret workflow er ikke i sig selv dokumentation for beståede eksterne kørsler; se repositoryets Actions-fane for status.

> [!IMPORTANT]
> Rigtig Ollama-inference er ikke udført i dette arbejdsmiljø. Modelkald i testene er simulerede. Retrievalkvalitet, korrekte kildehenvisninger, afvisninger og svartid skal kontrolleres med de faktiske modeller på undervisningscomputeren.

## Før undervisning

1. Følg [opsætningen](setup.md), og kontrollér at begge modeller findes i `ollama list`.
2. Kør de ti spørgsmål fra `evaluation_questions.json`.
3. Gem evidens og svar, og bedøm dem efter [evalueringsvejledningen](teaching.md#evaluering).
4. Tilføj en tekstfil, genstart, og kontrollér at et nyt faktum findes.
5. Notér modelnavne, hardware og eventuelle fejl i klassens resultater.
