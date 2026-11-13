#!/usr/bin/env python3
"""Print an AI-notes file shipped with the CFDEMcoupling documentation.

Usage:
    scripts/ai_notes.py [--docs online|<path>] [<name>]

<name> is a file below `<docs>/coupling/src/ai/` (default: INDEX.md; `.md` may be omitted).
The notes belong to the CFDEMcoupling code and are versioned with it, so the notes of the installed
Aspherix/CFDEM match the installed version. They are only read from a local documentation directory
(same source resolution as the other scripts, see doc_source.py; exit code 3 = unresolved, ask the user).
"""
import sys
from pathlib import Path

from doc_source import read, resolve, split_docs_arg


def main():
    choice, args = split_docs_arg(sys.argv[1:])
    name = args[0] if args else "INDEX.md"
    if not name.endswith(".md"):
        name += ".md"
    base, label, local = resolve("coupling", choice)
    if not local:
        sys.exit("AI_NOTES_UNAVAILABLE: the AI notes are not published on the website; use the installed "
                 "documentation or --docs <path> to a local documentation directory.")
    page = "src/ai/" + name
    if not (Path(base) / page).is_file():
        sys.exit(f"AI_NOTES_NOT_FOUND: {Path(base) / page} does not exist. This install may predate the AI "
                 "notes (or the name is wrong); list the folder, and fall back to the reference pages "
                 "(scripts/doc_index.py, scripts/fetch_section.py).")
    text, _ = read("coupling", page, choice)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
