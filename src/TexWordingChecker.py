"""
======================================================
 TeX Wording Checker
======================================================

 Kompetenztraining – HT 2025
 Autor   : Thai Tung Huynh
 Matr.-Nr: 1245059
 Betreuer: Herr Alexander Pascal Frank
 Datum   : 22.09.2025

======================================================
"""
import argparse
import json
from pathlib import Path

def checkTexFile(wordDict, visitedPath, currentFilePath):

    def replaceStr(textToReplace):
        for (k, v) in wordDict.items():
            if k in textToReplace:
                textToReplace = textToReplace.replace(k, v)
        return textToReplace


    # Get absolute path using Path(...).resolve()
    currentFilePath = Path(currentFilePath).resolve()

    # Avoid infinite recursion (loops)
    if currentFilePath in visitedPath:
        return

    visitedPath.add(currentFilePath)

    with open(currentFilePath, 'r', encoding="utf-8") as f:
        contentInLatex = f.read()

    lines = contentInLatex.splitlines()
    checkedLines = []

    # Flag to mark ignored environment
    ignoredLine = False 
    currentIgnoredCommand = ""
    pairNeedToIgnore = {
                 "\\begin{verbatim}": "\\end{verbatim}",
                 "\\begin{math}": "\\end{math}",
                 "\\begin{lstlisting}": "\\end{lstlisting}"}
    
    needToCheck = ["\\", "$", "%"]
    
    pairBracket = {"{": "}", "|": "|"}
    

    for line in lines:

        posInLine = 0
        newLine = ""

        while posInLine < len(line):
            currentStringCanReplace = ""

            while posInLine < len(line) and line[posInLine] not in needToCheck:
                currentStringCanReplace += line[posInLine]
                posInLine += 1

            if not ignoredLine:
                newLine += replaceStr(currentStringCanReplace)
            else:
                newLine += currentStringCanReplace # Do not replace inside ignored environment


            if posInLine == len(line):
                break

            if line[posInLine] == "%":
                newLine += line[posInLine:]
                break

            if line[posInLine] == "$":
                stringCanNotReplace = "$"
                posInLine += 1
                while posInLine < len(line):
                    stringCanNotReplace += line[posInLine]
                    if line[posInLine] == "$" and line[posInLine - 1] != "\\":
                        break
                    posInLine += 1

                newLine += stringCanNotReplace
                posInLine += 1
                continue

            if line[posInLine] == "\\":

                # Check if backslash is for \\, \$, \%
                if posInLine + 1 < len(line) and line[posInLine + 1] in needToCheck:
                    newLine += line[posInLine] + line[posInLine + 1]
                    posInLine += 2
                else:
                    # Parse LaTeX command name
                    latexCommand = ""
                    posInLine += 1
                    while posInLine < len(line) and line[posInLine].isalpha():
                        latexCommand += line[posInLine]
                        posInLine += 1

                    if line[posInLine] not in pairBracket:
                        newLine += "\\" + latexCommand
                        continue

                    # Extract content inside brackets
                    commandContent = ""
                    leftBracket = line[posInLine]
                    posInLine += 1 # go through bracket
                    while posInLine < len(line) and (line[posInLine] != pairBracket[leftBracket] or line[posInLine - 1] == "\\"):
                        commandContent += line[posInLine]
                        posInLine += 1

                    cmdLatex = "\\" + latexCommand + leftBracket + commandContent + pairBracket[leftBracket]
                    newLine += cmdLatex
                    posInLine += 1


                    # Check if command refers to another .tex file
                    if latexCommand == "input" or latexCommand == "include":
                        nextLatexFile = Path(currentFilePath.parent, commandContent + ".tex")
                        if nextLatexFile.exists():
                            checkTexFile(wordDict, visitedPath, nextLatexFile)


                    if ignoredLine and cmdLatex == pairNeedToIgnore[currentIgnoredCommand]:
                        ignoredLine = False
                        currentIgnoredCommand = ""
                        continue

                    # Verbatim environment can be skipped, since cmdLatex already contains the entire text between | |

                    # Check cmdLatex
                    if cmdLatex in pairNeedToIgnore:

                        if pairNeedToIgnore[cmdLatex] in line:
                            stringCanNotReplace = ""
                            while posInLine < len(line):
                                if line[posInLine: posInLine + len(pairNeedToIgnore[cmdLatex])] == pairNeedToIgnore[cmdLatex]:
                                    break
                                stringCanNotReplace += line[posInLine]
                                posInLine += 1

                            newLine += stringCanNotReplace + pairNeedToIgnore[cmdLatex]
                            posInLine += len(pairNeedToIgnore[cmdLatex])
                        else:
                            ignoredLine = True
                            currentIgnoredCommand = cmdLatex

        checkedLines.append(newLine)

    # Overwrite the original file with modified content
    newContentInLatex = "\n".join(checkedLines)
    with open(currentFilePath, 'w', encoding="utf-8") as f:
        f.write(newContentInLatex)

def readwordDictFromFile(pathFromwordDict):
    try:
        with open(pathFromwordDict, 'r', encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("File not found!")

def main():

    ORIGINAL_LIST_FROM_PATH = set()

    parser = argparse.ArgumentParser(
        description="TeX Wording Checker – vereinheitlicht Schreibweisen in LaTeX-Dateien."
    )
    parser.add_argument(
        "--config", "-c", required=True, help="Pfad zur Konfigurationsdatei (JSON)."
    )
    parser.add_argument(
        "--root", "-r", required=True, help="Wurzeldatei des LaTeX Projekts (.tex)."
    )

    args = parser.parse_args()

    checkTexFile(readwordDictFromFile(args.config), ORIGINAL_LIST_FROM_PATH, args.root)



if __name__ == '__main__':
    main()
