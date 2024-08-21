## Robot Template

Dette er ikke en pakke. Det er et template. Brug copy paste

### Filstruktur
- I starten, kan det være svært at vide hvad der er en god ide at enkapsulere. Af hensyn til nem kørsel, kan det være en god ide at køre alt i en fil inkl funktionerne. 
- main.py ligger lokalt hos udvikleren. Commit ofte til github.
- data, logs, .env ligger i automatikoutput. passwords ligger i pam.

### Vejledning til udarbejdelse af docs. 

- Hvorfor gør vi det? Fx "Så timelønnede kan få udbetalt pension" 
- Få styr på dine datakilder. Hvor kommer info fra og hvad indeholder det af data. Hvilken periode? Indeholde kilden alt den information der er behov for, til at producere output?  
- Transformer data fra datakilder til et format hvor du ved hvad 1 række er. Evt flere tabeller. Gem gerne data op SQL serveren. 
- Beskriv hvad der skal gøres, uafhængigt af hvordan. Fx alder under 21, lnklasse 001 skal ikke undersøges.
- Husk output skal ikke afhænge timing, men af input. Så gør perioden explicit eller afhængig af input, men ikke kørselstidspunkt.  
  


### Dependencies

## os2apwrapper installation

Hvis pip ikke kan installere fra `pip install -r requirements.txt`, så kør github pakkerne individuelt:

```console
pip install os2apwrapper@git+https://github.com/BorholmsRegionsKommuneIT/os2apwrapper@main
pip install brkrpautils@git+https://github.com/BorholmsRegionsKommuneIT/brkrpautils@main
```

### Update git pakker
To update you'll need to add the `--force-reinstall` parameter to the pip install command. This command can also be used as the install command.
```console
pip install --force-reinstall os2apwrapper@git+https://github.com/BorholmsRegionsKommuneIT/os2apwrapper@main
```
If you don't want to also reinstall the dependencies you can add the following parameter `--no-deps`.

If your project is using older versions of the packages that this project is using, you might need to add the `--upgrade` parameter in between `install` and `--force-reinstall`.