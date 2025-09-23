# Aufgaben

## User Interface
- Zuordnung von unterschiedlichen Schreibweisen in einer Konfigurationsdatei die in einem strukturierten Format (z.B. JSON) vorliegt,
- Kommandozeilenapplikation: Eingabe besteht aus Konfigurationsdatei sowie der Wurzeldatei des LaTeX Projekts
- Dokumentation
  - README Datei (Installation, Verwendung)
  - Kommandozeilen Hilfe (Erklärung der Parameter)

## Wortersetzung
- Beachtung von Groß- und Kleinschreibung (z.B. User-Data -> Userdata funktioniert auch für user-data)
- Ersetzung findet in regulären LaTeX Umgebungen statt, ausgenommen sind
  - Mathemathische Umgebungen ($$, equation)
  - Verbatim Umgebungen (verbatim, listings)
  - Kommandosequenzen (\somecommand)
  - Kommentare
- Ersetzung wird in-Place durchgeführt, resultat ist die neu geschriebene Datei

## Dateibearbeitung
- Ausgehend von einer LaTeX Wurzeldatei
- Automatisches hinzufügen aller durch \input oder \include hinzugefügten Dateien
  - Dabei auflösen von relativen bzw. absoluten imports

## Versionierung
- Verwendung von GitLab

## Testen
- Anhand eines LaTeX Projektes testen und Programm verifizieren
  
