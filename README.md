# Anleitung für Studentische Arbeiten

Von Ihrem Betreuer ist Ihnen ein Repository in einer der folgenden Gruppen zugewiesen worden:

- [Athene2 BA](https://athene2.informatik.unibw-muenchen.de/studarb/ba) für Bachelorarbeiten
- [Athene2 MA](https://athene2.informatik.unibw-muenchen.de/studarb/ba) für Masterarbeiten
- [Athene2 KP](https://athene2.informatik.unibw-muenchen.de/studarb/kp) für Kompetenztrainings

**Verändern Sie die Struktur und Namen der bestehenden Ordner und Dateien nicht.** Sie können nach Bedarf weitere Ordner und Dateien anlegen.

```
root
|-> abgaben                 # Ordner zur Abgabe der finalen PDFs für Vortrag und Abschlussarbeit
|-> ausarbeitung            # LaTeX Template für die MA/BA/KP Arbeit
|-> informationsmaterial    # Informationen für Studierende
|-> project.ini             # Metadaten dieser Arbeit
|-> README.md               # Dieses Dokument
|-> vortrag                 # Src Dateien für den Abschlussvortrag
``` 

## Erste Schritte

1. In Ihrem Hauptordner befindet sich eine project.ini Datei. Befüllen Sie diese Datei mit den auf Sie zutreffenden Informationen und halten Sie die Datei **jederzeit aktuell** sollte es zu Änderungen kommen.

2. Im Ordner `informationsmaterial` finden Sie das Merkblatt der Professur: `Merkblatt-fuer-BA-MA-Hommel.pdf`. Füllen Sie dieses Merkblatt aus und laden Sie eine unterschriebene Kopie im Ordner `abgaben` hoch. Sie dürfen die Datei alternativ auch digital signieren.

3. Machen Sie sich mit der Benutzung von git vertraut. Nutzen Sie die [Online Dokumentation](https://git-scm.com/doc). Für alle gängigen Betriebssysteme existieren als Alternative zur Bedienung per Kommandozeile auch grafische Bedienoberflächen.

## Fertige Dokumente/Artefakte
Sobald ein Dokument fertiggestellt wurde, wird die finale Datei (i.d.R. als PDF) einmalig im Ordner Abgaben abgelegt. Dabei wird die schriftliche Ausarbeitung als `nachname-matrikelnummer-thesis.pdf` hinterlegt, die Folien des Abschlussvortrags als `nachname-matrikelnummer-final-presentation.pdf`. Im Ordner `informationsmaterial` finden Sie zudem `Veroeffentlichung-BA-MA.pdf`. Füllen Sie dieses Informationsblatt aus und laden Sie eine ausgefüllte Kopie im Ordner `abgaben` hoch.

## LaTex Ausarbeitung
Die `.tex` Dateien sowie Ressourcen die benötigt werden um die Arbeit zu bauen werden im Ordner `ausarbeitung` abgelegt. Achten Sie auf regelmäßige Commits und vergesse Sie das Pushen nicht. Ein Grundlegendes `.gitignore` liegt bei, passen Sie es bei Bedarf an um volatile Dateien von der Versionierung auszuschließen.

Eine LaTeX Vorlage, die für alle Arbeiten von dieser Professur verwendet wird ist bereits in diesem Ordner hinterlegt.

## Ende der Studentischen Arbeit
Überprüfen Sie die `project.ini`. Das Projekt sollte den Status *Abgeschlossen* haben. Überprüfen Sie, dass mindestens alle fertigen Dokumente wie oben Beschrieben hinterlegt sind.

## Zusätzliche Fragen
Bei weiteren Fragen wenden Sie sich direkt an Ihren jeweiligen Betreuer.

## Checkliste
Folgende Checkliste hilft Ihnen die wichtigsten Schritte während der Arbeit im Auge zu behalten.

### Projektbeginn

- [ ] `project.ini` befüllt
- [ ] `Merkblatt-fuer-BA-MA-Hommel.pdf` unterschrieben und hochgeladen

### Projektende
- [ ] `project.ini` aktualisiert
- [ ] `nachname-matrikelnummer-thesis.pdf` hochgeladen
- [ ] `nachname-matrikelnummer-final-presentation.pdf` hochgeladen
- [ ] `Veroeffentlichung-BA-MA.pdf` ausfüllen und hochgeladen

