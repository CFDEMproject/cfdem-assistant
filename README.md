# CFDEM Assistant

An AI skill that helps with the setup of OpenFOAM-based [CFDEM®](https://doc.aspherix-dem.com/coupling/) solvers — simulations that couple OpenFOAM CFD with the [Aspherix®](https://www.aspherix-dem.com/) DEM solver.

It targets OpenFOAM 10 (the only version the current CFDEM coupling supports), points agents at the public CFDEM coupling documentation, and packages dictionary-, model-family-, and command-specific guidance that's tedious to look up by hand.
It's a companion to [Aspherix Assistant](https://github.com/CFDEMproject/aspherix-assistant): Aspherix Assistant covers the DEM side of a coupled case (the `.asx` input script), this skill covers the CFD side and the coupling layer itself.

## Install

This skill follows the [Agent Skills](https://agentskills.io) open standard, so the same `SKILL.md` works across Claude Code, Cursor, Gemini CLI, and Google Antigravity — only the install directory differs per tool.
See [`INSTALLATION.md`](INSTALLATION.md) for exact per-tool install paths and methods.

## What's in here

- `SKILL.md` — the skill definition: context, links to the public CFDEM coupling [docs](https://doc.aspherix-dem.com/coupling/), and pointers into `references/`.
- `scripts/ai_notes.py` — prints the CFDEM notes (rules, environment, solvers, `couplingProperties`, models, commands, coupling strategies). The notes are *not* in this repo: they live in the CFDEMcoupling repository (`documentation/coupling/src/ai/`) and ship with the installed documentation, so they are versioned with the code they describe.
- `references/OPENFOAM.md` — a short, deliberately thin list of links to official OpenFOAM 10 documentation.
- `references/CFDEM_DOC_SEARCH.md` — how to search and fetch the right page from the CFDEM coupling documentation.
- `references/commands/<name>.md` — per-command guidance for OpenFOAM utilities (`checkMesh`, `foamDictionary`, …), one file per command.
- `references/strategies/STRATEGIES.md` — version-independent problem-solving strategies; larger ones get their own `references/strategies/<name>.md` file.
- `scripts/doc_source.py` — resolves the docs source: the documentation of the installed Aspherix (via the `aspherix` binary) by default, `--docs online|<path>` or `$ASPHERIX_DOC_BASE` to override, exit code 3 when it can't be resolved. Shared by the two scripts below; keep in sync with Aspherix Assistant's copy.
- `scripts/doc_index.py` — reads and decompresses the docs' `objects.inv`, optionally filtered by keyword; used by `CFDEM_DOC_SEARCH.md`.
- `scripts/fetch_section.py` — reads a docs page and extracts one or more `<section id="...">` blocks verbatim, no model involved; used by `CFDEM_DOC_SEARCH.md`.

See `CLAUDE.md` for the conventions used when extending this repo.

## Trademarks

"CFDEM", "CFDEM®", "Aspherix", and "Aspherix®" are trademarks of DCS Computing GmbH, Linz.
This is documentation/tooling that references the public CFDEM coupling documentation; it is not the CFDEMcoupling or Aspherix software itself. See `LICENSE` for details.

## License

MIT — see `LICENSE`.
