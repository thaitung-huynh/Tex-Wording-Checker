\ProvidesClass{template}[2022/02/18, Abschlussarbeitstemplate, Universitaet der Bundeswehr Muenchen]

\LoadClass[bibliography=totoc,listof=totoc,BCOR=5mm,DIV=12]{scrbook}

% Sinnvolle Pakete
\RequirePackage[ngerman]{babel} % Trennung nach neuer deutscher Rechtschreibung, deutsche Sonderzeichen, z.B. \glqq und \grqq für deutsche Anführungszeichen
% Wenn auf Englisch geschrieben wird: ngerman durch english ersetzen. Unten in den Backmatters Abkürzungsverzeichnis in Abbreviations ändern.
\RequirePackage[utf8]{inputenc} % Umlaute im Text
\RequirePackage{graphicx} % Einfügen von Grafiken  - für PDF-Latex: .pdf und .png (.jpg möglich, sollte aber vermieden werden)
\RequirePackage{url}      % URLs (z.B. in Literatur) schöner formatieren
\RequirePackage{hyperref} % sorgt für für Hyperlinks in PDF-Dokumenten
\RequirePackage[parfill]{parskip}
\RequirePackage{ifthen}
\RequirePackage{acronym}

\graphicspath{{./Bilder/}}

\def\UrlBreaks{\do\/\do-}

% Chapter-Bibliographien
%\renewcommand{\StartFinalBibs}{\chapter*{\bibname}%
%\addcontentsline{toc}{chapter}{\bibname}%
%\@mkboth{\bibname}{\bibname}%
%\renewcommand{\bibname}{Literaturverzeichnis für Kapitel \thechapter}}

% Ersten Seiten
\def\frontmatter{
    \input{./Titel/titel-unibw} % Titelblätter UniBw
    \thispagestyle{empty}
    \cleardoublepage
    \thispagestyle{empty}
    \cleardoublepage
    \include{abstract} % Abstract
    \thispagestyle{empty}
    \tableofcontents % Inhaltsverzeichnis
}

\def\backmatter{
  \chapter*{Abkürzungsverzeichnis} % Wenn english: Abbreviations
  \addcontentsline{toc}{chapter}{Abkürzungsverzeichnis} % Wenn english: Abbreviations
  \input{abkuerzungen}
    \listoffigures
    \listoftables
    \bibliographystyle{alphadin} % Es gibt verschiedene Bibtex Styles, vgl. https://de.wikibooks.org/wiki/LaTeX-W%C3%B6rterbuch:_bibliographystyle. Ggf. muss alphadin hinzugefügt werden.
    \bibliography{./Bib/bib1} % Und hier ist die Bibtex-Datei eingebunden
    \input{./Titel/erklaerung-unibw} % Erklärung (Arbeit selbstständig verfasst)
}

\endinput
