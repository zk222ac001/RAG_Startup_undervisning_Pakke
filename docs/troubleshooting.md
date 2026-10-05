# 🛠️ Fejlfinding

[← Tilbage til forsiden](../README.md)

| Symptom | Sandsynlig årsag | Næste handling |
| :--- | :--- | :--- |
| `ollama` genkendes ikke | Ollama mangler eller terminalen har gammel PATH | Installér Ollama og genåbn terminalen |
| `Cannot connect to Ollama` | Den lokale server kører ikke | Åbn Ollama eller kør `ollama serve` i en anden terminal |
| “address already in use” ved `ollama serve` | En server bruger allerede porten | Prøv demoen med den eksisterende server |
| Model not found / 404 | Model mangler eller navnet er forkert | Kør `ollama list`, og download de to modeller fra opsætningsguiden |
| `ModuleNotFoundError` | Pakker og program bruger forskellig Python | Installér med `.venv`-Python som vist i opsætningsguiden |
| `py` genkendes ikke på Windows | Python launcher mangler | Kontrollér `python --version`; brug `python -m venv .venv`, hvis den viser 3.11+ |
| `No module named venv` på Linux | Distributionens venv-pakke mangler | Installér venv-understøttelse til din Python via distributionens pakkehåndtering |
| `Ollama timed out` eller meget langsomt svar | Modellen er langsom på computeren | Luk tunge programmer; prøv `llama3.2:1b` som beskrevet i opsætningen |
| Ingen tekststykker | Tomme filer, forkert format eller mappe | Tilføj ikke-tomme UTF-8 `.txt`-filer direkte i `data/` |
| Unicode-/læsefejl | Forkert kodning eller filadgang | Gem filen som UTF-8 i VS Code og kontrollér læserettigheder |
| Context-length-fejl | Et tekststykke har for mange tokens | Reducér `size` i `chunk_text`; ordantal er ikke tokenantal |
| Embedding count/dimensions-fejl | Ufuldstændigt svar eller blandede vektorer | Genstart og brug samme embeddingmodel til hele indekset |
| Svaret indeholder gamle oplysninger | Indekset ligger i RAM | Genstart efter ændringer i `data/` |
| Modellen opfinder fakta | Fundne kilder mangler fakta, eller modellen bruger dem forkert | Undersøg først evidensen, derefter prompten og modellen |
| Diagram vises som kode | Visningen understøtter ikke Mermaid | Åbn dokumentet på GitHub; SVG-oversigten kan også åbnes direkte |

> [!NOTE]
> En høj lighedsscore garanterer ikke et korrekt svar. En kildeetiket i svaret beviser heller ikke, at kilden understøtter påstanden.

## Hvis du ændrer modellen

Download først den nye model og opdatér den tilhørende konstant i `rag_demo.py`. Genstart, så dokumenter og spørgsmål bruger samme embeddingmodel. Gentag evalueringssættet; resultater kan ændre sig.

## Hvad demoen ikke gør

Den læser ikke PDF/Word, følger ikke undermapper og gemmer ikke indekset mellem kørsler. Den håndhæver ikke dokumentrettigheder og validerer ikke genererede kildehenvisninger automatisk. Brug den som læringsdemo med fiktive eller godkendte data.
