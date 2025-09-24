# TeX Wording Checker

Ein kleines Tool zur Vereinheitlichung von Schreibweisen in LaTeX-Datei.  
### Wortersetzung
- Beachtung von Groß- und Kleinschreibung (z.B. User-Data -> Userdata funktioniert auch für user-data)
- Ersetzung findet in regulären LaTeX Umgebungen statt, ausgenommen sind
  - Mathemathische Umgebungen ($$, equation)
  - Verbatim Umgebungen (verbatim, listings)
  - Kommandosequenzen (\somecommand)
  - Kommentare
- Ersetzung wird in-Place durchgeführt, resultat ist die neu geschriebene Datei

--- 
## Installation

- Projekt herunterladen via Git:
````text
    git clone "https://git.unibw.de/inf2-4/studarb/kp/huynh-1245059-0.git"
````

## Verwendung


```python
    python TexWordingChecker.py --config <CONFIG_DATEI> --root <HAUPT_DATEI>
```


## Kommandozeilen-Hilfe

```python
    python tex_checker.py --help
```
- Ausgabe
```text
    usage: TexWordingChecker.py [-h] --config CONFIG --root ROOT
    TeX Wording Checker – vereinheitlicht Schreibweisen in LaTeX-Dateien.
    
    options:
      -h, --help           show this help message and exit
      --config, -c CONFIG  Pfad zur Konfigurationsdatei (JSON).
      --root, -r ROOT      Wurzeldatei des LaTeX Projekts (.tex).
```
    

