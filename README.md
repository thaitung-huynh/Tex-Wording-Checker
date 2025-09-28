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
```bash
git clone "https://git.unibw.de/inf2-4/studarb/kp/huynh-1245059-0.git"
```

## Verwendung

- Ausführung mit: 
```bash
python TexWordingChecker.py --config <CONFIG_DATEI> --root <HAUPT_DATEI>
```

### Beispiel
- Config-JSON: 
```json
{
  "cyber_security": "Cyber Security",
  "cybersecurity": "Cyber Security",
  "cyb": "Cyber Security"
}
```
- Sample-Tex:
```latex
\documentclass{article}
\begin{document}

This paper is about cyber_security in modern society.
Some people also write cybersecurity or even cyb,
but they all mean the same thing.

We define that \textbf{cybersecurity} is a key concept in technology.
However, mistakes like \emph{cyb} or cyber_security are common.

\begin{verbatim}
Inside verbatim environment, words like cyber_security or cyb
should not be changed.
\end{verbatim}

Mathematical expression should stay the same: $a + b = c$ and
$\cyb + \cybersecurity = \text{secure}$.

\lstinline|cyber_security| should also remain unchanged.

\end{document}
```

## Kommandozeilen-Hilfe

- Ausführung mit: 
```bash
python TexWordingChecker.py --config <CONFIG_DATEI> --root <HAUPT_DATEI>
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
    

