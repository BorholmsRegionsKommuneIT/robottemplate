## Robot Template

Dette er ikke en pakke. Det er en template. Brug copy paste :-)


### Vejledning til udarbejdelse af docs.

- Hvorfor gør vi det? Fx "Så timelønnede kan få udbetalt pension"
- Få styr på dine datakilder før der udarbejdes docs. Hvor kommer info fra og hvad indeholder det af data. Hvilken periode? Indeholder kilden alt den information der er behov for, til at producere output?
- Transformer data fra datakilder til et format hvor du ved hvad en række er. Evt flere tabeller med veldefinerede relationer. Gem gerne data op på SQL serveren.
- Beskriv hvad der skal gøres, uafhængigt af hvordan. Fx "alder under 21", "manr med lnklasse 5678 skal ikke have pension - filtrer dem fra".
- Husk output skal ikke afhænge af kørselstidspunkt, men af input. Så gør perioden explicit i koden eller tilføj input fil. Brug ikke kørselstidspunkt til andet end `SESSION_ID`.
- fagperson leverer output som, udvikler skal reproducere. Output skal gerne indeholde tænkelige edge cases. 

### Dependencies with [uv](https://docs.astral.sh/uv/)

Pypi packages can be installed with:

```console
uv add requests
```

Install a git dependency:

```console
uv add brkrpautils --git https://github.com/BorholmsRegionsKommuneIT/brkrpautils
```

Declare a dependency and it's source in `pyproject.toml`:

```toml
[project]
dependencies = [
    "brkrpautils",
]

[tool.uv.sources]
brkrpautils = { git = "https://github.com/BorholmsRegionsKommuneIT/brkrpautils" }
```

And declare dev dependencies like this:

```toml
[tool.uv]
dev-dependencies = [
    "ruff",
    "ipykernel",
]
```

Create the virtual environment with the chosen Python version, and install all the dependencies, including the dev ones:

```console
uv venv --python 3.12
uv sync
```

