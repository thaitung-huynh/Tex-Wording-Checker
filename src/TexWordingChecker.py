"""
    ======================================================
                     TeX Wording Checker
    ======================================================
     Kompetenztraining – HT 2025
     Autor         : Thai Tung Huynh - INF24
     Matrikelnummer: 1245059
     Betreuer      : Herr Alexander Pascal Frank
     Datum         : 23.09.2025 - 07.10.2025
    ======================================================
"""
from pathlib import Path
import argparse
import json

# Initialization
pair_need_to_ignore = { "\\begin{verbatim}": "\\end{verbatim}",
                        "\\begin{math}": "\\end{math}",
                        "\\begin{lstlisting}": "\\end{lstlisting}",
                        "\\begin{equation}": "\\end{equation}",
                        }
need_to_check_again = ["\\", "$", "%"]
pairs = {"{": "}", "(": ")", "[": "]"}
# End-Initialization

def replace_string_in_tex(word_dict: dict, text_to_replace: str) -> str:
    """
        Replace specific substrings in a given text based on a dictionary of replacements

        This function performs string replacement operations on LaTeX text content,
        substituting incorrect words or phrases with their correct counterparts
        as defined in the provided dictionary. All matching substrings are replaced
        in a single pass through the dictionary.

        Parameters
        ----------
        word_dict      : dict
        text_to_replace: str
    """
    for (k, v) in word_dict.items():
        if k in text_to_replace:
            text_to_replace = text_to_replace.replace(k, v)
    return text_to_replace

def process_inline_math(line: str, pos_in_line: int) -> tuple[str, int]:
    """
        Handle LaTeX inline math environments delimited by dollar signs ($...$).

        This function extracts inline mathematical expressions from LaTeX source,
        preserving the math content unchanged since mathematical notation should
        not be subject to word corrections. It properly handles escaped dollar
        signs within the math environment.

        Parameters
        ----------
        line       : The LaTeX source line containing the inline math expression
        pos_in_line: Current position in the line (should be at the opening $ character)
    """
    result = "$"
    pos_in_line += 1
    while pos_in_line < len(line):
        result += line[pos_in_line]
        if line[pos_in_line] == "$" and line[pos_in_line - 1] != "\\":
            break
        pos_in_line += 1
    return result, pos_in_line + 1


def process_lstinline(line: str, pos_in_line: int) -> tuple[str, int]:
    """
        Handle the LaTeX \\lstinline command with custom delimiters.

        The \\lstinline command is used to display inline code in LaTeX and uses
        custom delimiters (e.g., \\lstinline#code# or \\lstinline|code|). The content
        between the delimiters should remain unchanged as it represents literal code.
        This function extracts the complete command including its delimited content.

        Parameters
        ----------
        line       : The LaTeX source line containing the \\lstinline command
        pos_in_line: Current position in the line (should be right after the backslash of \\lstinline)
    """
    # Skip \lstinline
    pos_in_line += 9  # len("lstinline") = 9

    if pos_in_line >= len(line):
        return "\\lstinline", pos_in_line

    # Get left delimiter
    delimiter = line[pos_in_line]
    result = "\\lstinline" + delimiter
    pos_in_line += 1

    # Find right delimiter
    while pos_in_line < len(line):
        result += line[pos_in_line]
        if line[pos_in_line] == delimiter:
            break
        pos_in_line += 1

    return result, pos_in_line + 1


def process_latex_command(line: str, pos_in_line: int, current_path: Path,
                          visited_path: set[Path], word_dict: dict,
                          ignored_line: bool, current_ignored_cmd: str) -> tuple[str, int, bool, str]:
    """
        Process LaTeX commands and handle special cases like includes and ignored environments.

        This function parses LaTeX commands starting with backslash (\\), extracts the command
        name and its arguments, and handles special behaviors for specific commands such as
        file inclusion and environment ignoring. It maintains proper bracket matching and
        state management for ignored sections.

        Parameters
        ----------
        line               : The LaTeX source line being processed
        pos_in_line        : Current position in the line (should be at the backslash character)
        current_path       : Path to the current file being processed
        visited_path       : Set of already visited file paths to prevent circular includes
        word_dict          : Dictionary for word corrections (passed to recursive file processing)
        ignored_line       : Current state indicating whether we're in an ignored section
        current_ignored_cmd: Name of the current LaTeX command/environment being ignored
    """
    latex_command = ""
    pos_in_line += 1

    # Read command name
    while pos_in_line < len(line) and line[pos_in_line].isalpha():
        latex_command += line[pos_in_line]
        pos_in_line += 1

    # Handle \lstinline specially
    if latex_command == "lstinline":
        res, pos = process_lstinline(line, pos_in_line)
        return res, pos, ignored_line, current_ignored_cmd

    # Simple case: no { after command
    if pos_in_line >= len(line) or line[pos_in_line] not in "{[(|":
        return "\\" + latex_command, pos_in_line, ignored_line, current_ignored_cmd

    left_bracket = line[pos_in_line]
    pos_in_line += 1
    content = left_bracket

    # Handle nested brackets
    bracket_count = 1
    while pos_in_line < len(line) and bracket_count > 0:
        char = line[pos_in_line]
        content += char

        if char == left_bracket:
            bracket_count += 1
        elif char == pairs[left_bracket]:
            bracket_count -= 1

        pos_in_line += 1

    # Handle include/input
    if latex_command in {"input", "include"}:
        next_file = Path(current_path.parent, content[1:-1] + ".tex")
        if next_file.exists():
            check_tex_file(word_dict, visited_path, next_file)


    # Handle ignored environments
    cmd_full = "\\" + latex_command + content
    if cmd_full in pair_need_to_ignore:
        ignored_line = True
        current_ignored_cmd = cmd_full

    if ignored_line and cmd_full == pair_need_to_ignore.get(current_ignored_cmd, ""):
        ignored_line = False
        current_ignored_cmd = ""

    return cmd_full, pos_in_line, ignored_line, current_ignored_cmd


def process_line(line: str, word_dict: dict, ignored_line: bool, current_ignored_cmd: str,
                 current_path: Path, visited_path: set[Path]) -> tuple[str, bool, str]:
    """
        Process a single line of LaTeX source code for word corrections and formatting.

        This function parses a LaTeX line character by character, handling different
        LaTeX elements (comments, math modes, commands) while applying word corrections
        from the dictionary only to appropriate text content. It maintains state about
        ignored sections to avoid modifying content that should remain unchanged.

        Parameters
        ----------
        line               : The LaTeX source line to be processed
        word_dict          : Dictionary containing word corrections (key: incorrect word, value: correct word)
        ignored_line       : Current state indicating whether the line is within an ignored section/environment
        current_ignored_cmd: Name of the current LaTeX command/environment being ignored
        current_path       : Path to the current file being processed
        visited_path       : Set of already visited file paths to prevent circular processing
    """
    # Initialization
    new_line = ""
    pos_in_line = 0

    while pos_in_line < len(line):
        current_replace_string = ""
        while pos_in_line < len(line and
              (line[pos_in_line] not in need_to_check_again or (pos_in_line != 0 and line[pos_in_line - 1] == "\\"))):
            current_replace_string += line[pos_in_line]
            pos_in_line += 1


        if not ignored_line:
            new_line += replace_string_in_tex(word_dict, current_replace_string)
        else:
            new_line += current_replace_string

        if pos_in_line >= len(line):
            break

        if line[pos_in_line] == "%":
            new_line += line[pos_in_line:]
            break

        elif line[pos_in_line] == "$":
            math_content, pos_in_line = process_inline_math(line, pos_in_line)
            new_line += math_content

        elif line[pos_in_line] == "\\":
            cmd, pos_in_line, ignored_line, current_ignored_cmd = process_latex_command(line, pos_in_line, current_path, visited_path,
                                                                                        word_dict, ignored_line, current_ignored_cmd)
            new_line += cmd

    return new_line, ignored_line, current_ignored_cmd


def check_tex_file(word_dict: dict, visited_path: set[Path], current_path: Path) -> None:
    """
        Check and process a LaTeX file for spell checking or formatting corrections.

        This function reads a LaTeX file, processes each line to check and correct
        errors based on the provided dictionary, then writes the processed content
        back to the original file. It includes a mechanism to avoid duplicate
        processing through the visited_path set.

        Parameters
        ----------
        word_dict   : Dictionary containing word corrections (key: incorrect word, value: correct word)
        visited_path: Set of already visited file paths to prevent circular processing
        current_path: Path to the current file being processed
    """
    current_path = Path(current_path).resolve()
    if current_path in visited_path:
        return
    visited_path.add(current_path)

    try:
        with open(current_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"File not found: {current_path}")
        return

    checked_lines = []
    ignored_line = False
    current_ignored_cmd = ""

    for line in lines:
        new_line, ignored_line, current_ignored_cmd = process_line(line, word_dict, ignored_line, current_ignored_cmd,
                                                                   current_path, visited_path)
        checked_lines.append(new_line)

    with open(current_path, "w", encoding="utf-8") as f:
        f.write("\n".join(checked_lines))

    # Notification for user
    print(f"> Processed  : {current_path}")



def read_dict(dict_path: Path) -> dict:
    """
        Read dictionary from JSON file.
        Parameters
        ----------
        dict_path: str
    """
    try:
        with open(dict_path, 'r', encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Configuration file not found: {dict_path}")


def main():
    """
        Main entry point for the TeX Wording Checker application.

        This function serves as the command-line interface for the TeX Wording Checker,
        which standardizes and corrects word usage in LaTeX documents. It parses
        command-line arguments, loads the configuration dictionary, and initiates
        the checking process on the specified LaTeX project.

        Command-line Arguments
        ----------------------
        --config, -c : str
            Path to the configuration file (.JSON) containing the word dictionary
            for corrections and standardizations
        --root, -r   : str
            Path to the root LaTeX file (.tex) of the project to be processed
    """
    # Command Config
    parser = argparse.ArgumentParser(
        description="TeX Wording Checker – vereinheitlicht Schreibweisen in LaTeX-Dateien."
    )
    parser.add_argument(
        "--config", "-c", required=True, help="Pfad zur Konfigurationsdatei(.JSON)."
    )
    parser.add_argument(
        "--root", "-r", required=True, help="Wurzeldatei des LaTeX Projekts(.tex)."
    )
    args = parser.parse_args()
    # End-Command Config

    word_dict = read_dict(args.config)

    root_path = args.root

    # CLI-UI
    print(f"======================================================\n"
          f"               TeX Wording Checker\n"
          f"======================================================\n"
          f"> Config-File: {Path(args.config).resolve()} \n"
          f"> Root-File  : {Path(args.root).resolve()}")
    # End - UI

    check_tex_file(word_dict, set(), root_path)
    print("Processing completed.")


if __name__ == '__main__':
    main()
# EOF - Tung - INF24