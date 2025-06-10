## Robot Template

Kør `uv init` og kopier `main` og `DOTENV_PATH`.

### Retningslinjer til dokumentation og udvikling
- Skriv dokumentationen i markdown. 
- Beskriv det overordnede formål.
- Adskil I/O fra forretningslogikken fra start. Selv hvis det ikke er smart fra et performance hensyn. Få styr på dine datakilder som noget af det første. Indeholder datakilden alt den information der er behov for, til at producere output?
- Transformer data fra datakilder til et format hvor du ved hvad en række er. Evt flere tabeller med veldefinerede relationer. 
- Brug tid på at få data input modeleret korrekt og få det typed. Brug med fordel dataclasses. 
- Gå efter deklerativ forretningslogik: beskriv hvad der skal gøres, ikke hvordan. Og frem for alt uafhængigt af I/O.
- Gør det helt tydeligt i docs hvad forskellen mellem kørsler er (typisk periode)  
- Husk output skal ikke afhænge af kørselstidspunkt, men af input. Derfor gør perioden explicit i koden eller tilføj input fil. Brug ikke kørselstidspunkt til andet end `SESSION_ID`.
- fagperson leverer data til output som, udvikler skal reproducere. Output skal gerne indeholde alle tænkelige edge cases. Fagpersonens ouput skal være så klart at, udvikler nemt kan omskrive det til tests. Output skal være et maskinlæsbart format. 
- Overvej at skrive en draft af robotten kun med log.info() statements.  
- omdøb ikke variable hvis det gør debugging svært!
- meningsfulde variabelnavne.
- Undgå store loops
- Undgå lange funktioner, brug *function composition* i stedet.
- når koden fylder et par hundrede linjer, overvej at splitte op i filer eller funktioner.
- A good practice is to handle expected errors inside functions (when recovery is possible) and let unexpected errors propagate so they can be caught at a higher level.
- God logning kan hjælpe i udviklingsfasen ved at beskrive detaljeret hvorfor en beslutning blev truffet og hvilke data der lå til grund. 

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
