#!/usr/bin/env python3
"""Print the AI notes of the CFDEMcoupling documentation.

Usage:
    scripts/ai_notes.py [--docs online|<path>]              # the notes of all pages
    scripts/ai_notes.py [--docs online|<path>] <page> ...   # the notes of the named pages

The notes belong to the CFDEMcoupling code and are versioned with it: they are HTML comments
(`<!-- AI-NOTE ... -->`) in the reference pages of the documentation, not rendered in a browser.
Plain HTML-to-text readers drop comments, so use this script (fetch_section.py also appends the
notes of the page it reads). <page> is a page of the coupling documentation, `.html` optional
(`cfdemSimulate`, `locateModel`, ...). Without a page the local documentation directory is
scanned; `--docs online` needs page names, as the website has no page list.
Pages not enabled by the licence are replaced by a placeholder in the installed documentation and
carry no notes: that is normal, not an error. Same source resolution as the other scripts, see
doc_source.py (exit code 3 = unresolved, ask the user).
"""
import re
import sys
from pathlib import Path

from doc_source import page_not_found, read, resolve, split_docs_arg

NOTE_RE = re.compile(r"<!-- AI-NOTE\n(.*?)\n-->", re.S)
FIRST = ["Section_gettingStarted"]  # general rules, listed first


def page_notes(html):
    """Return the texts of all AI-NOTE comments in an html page."""
    return [m.strip() for m in NOTE_RE.findall(html)]


def main():
    choice, args = split_docs_arg(sys.argv[1:])
    base, label, local = resolve("coupling", choice)
    if args:
        pages = [a if a.endswith(".html") else a + ".html" for a in args]
    elif local:
        found = sorted(p.name for p in Path(base).glob("*.html"))
        key = lambda n: (n[:-5] not in FIRST, n)
        pages = sorted(found, key=key)
    else:
        sys.exit("AI_NOTES_UNAVAILABLE: the website has no page list; name the pages "
                 "(scripts/ai_notes.py <page> ...) or use the installed documentation or "
                 "--docs <path> to a local documentation directory.")
    total = read_pages = 0
    for page in pages:
        try:
            html, _ = read("coupling", page, choice)
        except OSError as e:
            print(page_not_found("coupling", page, e), file=sys.stderr)
            continue
        read_pages += 1
        for note in page_notes(html):
            total += 1
            print(f"=== {page} ===\n{note}\n")
    if total:
        return
    if not read_pages:
        sys.exit(1)  # every named page was missing, reported above
    sys.exit("AI_NOTES_NOT_FOUND: the " + ("page carries" if read_pages == 1 else "pages carry")
             + " no AI notes in " + label + ". "
             + ("The online docs may predate the notes or not show them; use the installed "
                "documentation. " if not local else
                "This install may predate the notes, or these pages carry none. ")
             + "Fall back to the reference pages (scripts/doc_index.py, scripts/fetch_section.py).")


if __name__ == "__main__":
    main()
