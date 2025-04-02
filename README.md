## Robot Template

Dette er ikke en pakke. Det er en template for robotter. Kør `uv init` og kopier `main` og `DOTENV_PATH`. Brug copy paste :-)

### Vejledning til udarbejdelse af docs.

- Hvorfor gør vi det? Fx "Så timelønnede kan få udbetalt pension"
- Få styr på dine datakilder før der udarbejdes docs. Hvor kommer info fra og hvad indeholder det af data. Hvilken periode? Indeholder kilden alt den information der er behov for, til at producere output?
- Transformer data fra datakilder til et format hvor du ved hvad en række er. Evt flere tabeller med veldefinerede relationer. Gem gerne data op på SQL serveren.
- Beskriv hvad der skal gøres, uafhængigt af hvordan. Fx "alder under 21", "manr med lnklasse 5678 skal ikke have pension - filtrer dem fra".
- Husk output skal ikke afhænge af kørselstidspunkt, men af input. Så gør perioden explicit i koden eller tilføj input fil. Brug ikke kørselstidspunkt til andet end `SESSION_ID`.
- fagperson leverer output som, udvikler skal reproducere. Output skal gerne indeholde tænkelige edge cases.

### Kodestil

- omdøb ikke variable hvis det gør debugging svært!
- meningsfulde variabelnavne.
- når koden fylder et par hundrede linjer, overvej at splitte op i filer eller funktioner, men ikke et must.
- A good practice is to handle expected errors inside functions (when recovery is possible) and let unexpected errors propagate so they can be caught at a higher level.
- God logning kan hjælpe i udviklingsfasen og ved debugging efter deployment.

### Dependencies with [uv](https://docs.astral.sh/uv/)

Pypi packages can be added with:

```console
uv add requests
```

Add a git dependency:

```console
uv add "brkrpautils @ git+https://github.com/BorholmsRegionsKommuneIT/brkrpautils"
```

Syncing the env with `uv sync` or just run with `uv run` and the sync happen automagically.
