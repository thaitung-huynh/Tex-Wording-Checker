#Tung Huynh - Kompetenztraining - HT25
import argparse
import json
from pathlib import Path

def checkTexFile(dict, listFromPath, currentFilePath):

    def replaceStr(textToReplace):
        for (k, v) in dict.items():
            if k in textToReplace:
                textToReplace = textToReplace.replace(k, v)
        return textToReplace

    #Get absolute Path with Path(...).resolve()
    currentFilePath = Path(currentFilePath).resolve()

    # Avoid loop
    if currentFilePath in listFromPath:
        return

    listFromPath.add(currentFilePath)

    with open(currentFilePath, 'r', encoding="utf-8") as f:
        contentInLatex = f.read()

    lines = contentInLatex.splitlines()
    checkedLines = []
    ignoredLine = False #Flag
    leftIgnore = ""
    pairToIgnore = {
                 "\\begin{verbatim}": "\\end{verbatim}",
                 "\\begin{math}": "\\end{math}",
                 "\\begin{lstlisting}": "\\end{lstlisting}"}

    pairBracket = {"{": "}", "|": "|"}

    needToCheck = ["\\", "$", "%"]

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
                newLine += currentStringCanReplace # Now it can not be replaced


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
                    # Get command
                    latexCommand = ""
                    posInLine += 1
                    while posInLine < len(line) and line[posInLine].isalpha():
                        latexCommand += line[posInLine]
                        posInLine += 1

                    if line[posInLine] not in pairBracket:
                        newLine += "\\" + latexCommand
                        continue

                    # Get content
                    commandContent = ""
                    leftBracket = line[posInLine]
                    posInLine += 1 # go through bracket
                    while posInLine < len(line) and (line[posInLine] != pairBracket[leftBracket] or line[posInLine - 1] == "\\"):
                        commandContent += line[posInLine]
                        posInLine += 1

                    cmdLatex = "\\" + latexCommand + leftBracket + commandContent + pairBracket[leftBracket]
                    newLine += cmdLatex
                    posInLine += 1

                    # Now position from posInLine at the end of command \begin{...} <-

                    # Check if command for another .tex
                    if latexCommand == "input" or latexCommand == "include":
                        nextLatexFile = Path(currentFilePath.parent, commandContent + ".tex")
                        if nextLatexFile.exists():
                            checkTexFile(dict, listFromPath, nextLatexFile)


                    if ignoredLine and cmdLatex == pairToIgnore[leftIgnore]:
                        ignoredLine = False
                        leftIgnore = ""
                        continue

                    # Check if command is verbatim-environment
                    if latexCommand == "verb":
                        continue # because cmdLatex contains all text between | |

                    if cmdLatex in pairToIgnore:

                        if pairToIgnore[cmdLatex] in line:
                            stringCanNotReplace = ""
                            while posInLine < len(line):
                                if line[posInLine: posInLine + len(pairToIgnore[cmdLatex])] == pairToIgnore[cmdLatex]:
                                    break
                                stringCanNotReplace += line[posInLine]
                                posInLine += 1

                            newLine += stringCanNotReplace + pairToIgnore[cmdLatex]
                            posInLine += len(pairToIgnore[cmdLatex])
                        else:
                            ignoredLine = True
                            leftIgnore = cmdLatex

        checkedLines.append(newLine)

    # Overwrite old content
    newContentInLatex = "\n".join(checkedLines)
    with open(currentFilePath, 'w', encoding="utf-8") as f:
        f.write(newContentInLatex)

def readDictFromFile(pathFromDict):
    try:
        with open(pathFromDict, 'r', encoding="utf-8") as f:
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

    checkTexFile(readDictFromFile(args.config), ORIGINAL_LIST_FROM_PATH, args.root)



if __name__ == '__main__':
    main()
