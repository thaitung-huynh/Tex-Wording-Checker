#Tung Huynh - Kompetenztraining - HT25
import argparse
import json
from pathlib import Path

def checkTexFile(dict, listFromPath, currentFilePath):

    def splitCommand(lineInLatex):
        cmd = ""
        content = ""
        i = 1
        while i < len(lineInLatex):
            if lineInLatex[i] == "{":
                content += lineInLatex[i + 1]
                i += 2
                continue
            if lineInLatex[i] == "}":
                break

            if content == "":
                cmd += lineInLatex[i]
            else:
                content += lineInLatex[i]
            i += 1
        return cmd, content

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

    for line in lines:
        if line.startswith(("\\", "%")):
            cmd, nextPath = splitCommand(line)
            # Check if it contains include then check new file
            if cmd == "include":
                nextLatexFile = Path(currentFilePath.parent, nextPath + ".tex")
                if nextLatexFile.exists():
                    checkTexFile(dict, listFromPath, nextLatexFile)

            checkedLines.append(line)
        else:
            inMathExp = False
            newLine = ""
            mathExp = ""
            textToFix = ""

            for i in range(len(line)):
                if line[i] == "%":
                    newLine += replaceStr(textToFix) + line[i:]
                    textToFix = ""
                    break

                if line[i] == "$" and not inMathExp and (i == 0 or line[i - 1] != "\\"):
                    inMathExp = True
                    mathExp = "$"
                    newLine += replaceStr(textToFix)
                    textToFix = ""
                else:
                    if not inMathExp:
                        textToFix += line[i]
                    else:
                        mathExp += line[i]

                    if inMathExp and line[i] == "$" and (i > 0 and line[i - 1] != "\\"):
                        inMathExp = False
                        newLine += mathExp
                        mathExp = ""

            # Last check, if it doesn't contain $
            if textToFix != "":
                newLine += replaceStr(textToFix)
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
