"""Resolve where to read the Aspherix documentation from.

Default: the documentation shipped with the installed Aspherix, found relative to the `aspherix`
binary on PATH (<bin>/../documentation/<product>/). It matches the installed version; the website
always shows the latest release. The source in use is announced on stderr.

Explicit choice, which wins over the default (flag over env var):
    --docs online        the website https://doc.aspherix-dem.com/ (version / licence may differ)
    --docs <path>        a local documentation directory containing <product>/ (e.g. a dev build)
    $ASPHERIX_DOC_BASE   the same values, for a persistent choice

If there is no explicit choice and no `aspherix` binary (or no docs next to it), the scripts exit
with code 3 and a message starting DOCS_SOURCE_UNRESOLVED, without guessing and without network
access. Scripts cannot prompt: the calling agent asks the user and re-runs with --docs.

Products: solver, coupling, calibration, gui, main.
"""
import os
import shutil
import sys
import urllib.request
from pathlib import Path

ONLINE = "https://doc.aspherix-dem.com/"
EXIT_UNRESOLVED = 3
_announced = set()


def split_docs_arg(args):
    """Remove `--docs X` / `--docs=X` from args; return (choice or None, remaining args)."""
    rest, choice, i = [], None, 0
    while i < len(args):
        if args[i] == "--docs":
            if i + 1 >= len(args):
                sys.exit("--docs needs a value: online or a documentation directory")
            choice, i = args[i + 1], i + 2
        elif args[i].startswith("--docs="):
            choice, i = args[i][len("--docs="):], i + 1
        else:
            rest.append(args[i])
            i += 1
    return choice, rest


def resolve(product, choice=None):
    """Return (base, label, is_local); base ends in '/'. Exits with EXIT_UNRESOLVED if undecidable."""
    choice = choice or os.environ.get("ASPHERIX_DOC_BASE")
    if choice == "online":
        return ONLINE + product + "/", "ONLINE docs (explicit choice)", False
    if choice:
        d = Path(choice).expanduser() / product
        if not d.is_dir():
            sys.exit(f"--docs / $ASPHERIX_DOC_BASE: {d} does not exist (expected a documentation "
                     f"directory containing {product}/)")
        return str(d) + "/", f"local docs {d} (explicit choice)", True
    exe = shutil.which("aspherix")
    if exe:
        d = Path(exe).resolve().parent.parent / "documentation" / product
        if d.is_dir():
            return str(d) + "/", f"installed docs {d} (derived from the aspherix binary {exe})", True
        why = f"the aspherix binary {exe} has no {d} next to it"
    else:
        why = "no `aspherix` binary found on PATH"
    print(f"DOCS_SOURCE_UNRESOLVED: {why}, so the installed documentation cannot be located.\n"
          "Ask the user which to use, then re-run with --docs:\n"
          "  --docs online  : the online docs (doc.aspherix-dem.com). Latest release - the version, or "
          "features enabled by the licence, may differ from the user's Aspherix.\n"
          "  --docs <path>  : a local documentation directory containing <product>/ (e.g. a developer build).\n"
          "Alternatively put `aspherix` on PATH (e.g. source the installer's shell_variables.sh).",
          file=sys.stderr)
    sys.exit(EXIT_UNRESOLVED)


def read(product, page, choice=None, binary=False):
    """Read `page` of `product` docs. Returns (data, label). Raises OSError if the page is missing."""
    base, label, local = resolve(product, choice)
    if label not in _announced:
        _announced.add(label)
        print(f"# Using {label}", file=sys.stderr)
        if not local:
            print("# NOTE: the online docs show the latest release and may differ from the installed "
                  "Aspherix/CFDEM version (commands, options, defaults, licence-enabled features); "
                  "verify version-sensitive details.", file=sys.stderr)
    if local:
        data = (Path(base) / page).read_bytes()
    else:
        with urllib.request.urlopen(base + page, timeout=60) as resp:
            data = resp.read()
    return (data if binary else data.decode("utf-8", errors="replace")), label
