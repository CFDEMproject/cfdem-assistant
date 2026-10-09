# CFDEM Assistant

An AI skill that helps with the setup of OpenFOAM-based [CFDEM®](https://doc.aspherix-dem.com/coupling/) solvers — simulations that couple OpenFOAM CFD with a DEM particle solver (LIGGGHTS/[Aspherix®](https://www.aspherix-dem.com/)).

It targets OpenFOAM 10 (the only version the current CFDEM coupling supports), points agents at the public CFDEM coupling documentation, and packages dictionary-, model-family-, and command-specific guidance that's tedious to look up by hand.
It's a companion to [Aspherix Assistant](https://github.com/CFDEMproject/aspherix-assistant): Aspherix Assistant covers the DEM side of a coupled case (the `.asx`/LIGGGHTS input script), this skill covers the CFD side and the coupling layer itself.

## Install

This skill follows the [Agent Skills](https://agentskills.io) open standard, so the same `SKILL.md` works across Claude Code, Cursor, Gemini CLI, and Google Antigravity — only the install directory differs per tool.
See [`INSTALLATION.md`](INSTALLATION.md) for exact per-tool install paths and methods.

## What's in here

- `SKILL.md` — the skill definition: context, links to the public CFDEM coupling [docs](https://doc.aspherix-dem.com/coupling/), and pointers into `references/`.
- `references/RULES.md` — the single source of truth for rules every CFDEM-coupled case must follow.
- `references/OPENFOAM.md` — a short, deliberately thin list of links to official OpenFOAM 10 documentation.
- `references/SOLVERS.md` — the available `cfdemSolver*` binaries, what each is for, and which are gated behind licensing.
- `references/CFDEM_DOC_SEARCH.md` — how to search and fetch the right page from the public CFDEM coupling documentation.
- `references/CFDEM_ENVIRONMENT.md` — loading the CFDEM environment (`bashrc`/`zshrc`), and its environment variables and aliases.
- `references/commands/<name>.md` — per-command guidance (styles, syntax, examples, preferred usage) for OpenFOAM utilities (`checkMesh`, `foamDictionary`, …) and CFDEM's own utilities (`cfdemSimulate`, …), one file per command.
- `references/dictionaries/<name>.md` — per-dictionary reference for a CFDEM coupling dictionary (e.g. `couplingProperties`), one file per dictionary.
- `references/models/<name>.md` — per-model-family reference (e.g. `forceModels`, `voidFractionModels`, `smoothingModels`).
- `references/strategies/STRATEGIES.md` — short problem-solving strategies for building and debugging coupled cases; larger ones get their own `references/strategies/<name>.md` file.
- `scripts/doc_source.py` — resolves the docs source: the documentation of the installed Aspherix (via the `aspherix` binary) by default, `--docs online|<path>` or `$ASPHERIX_DOC_BASE` to override, exit code 3 when it can't be resolved. Shared by the two scripts below; keep in sync with Aspherix Assistant's copy.
- `scripts/doc_index.py` — reads and decompresses the docs' `objects.inv`, optionally filtered by keyword; used by `CFDEM_DOC_SEARCH.md`.
- `scripts/fetch_section.py` — reads a docs page and extracts one or more `<section id="...">` blocks verbatim, no model involved; used by `CFDEM_DOC_SEARCH.md`.

See `CLAUDE.md` for the conventions used when extending this repo.

## Trademarks

"CFDEM", "CFDEM®", "Aspherix", and "Aspherix®" are trademarks of DCS Computing GmbH, Linz.
This is documentation/tooling that references the public CFDEM coupling documentation; it is not the CFDEMcoupling or Aspherix software itself. See `LICENSE` for details.

## License

MIT — see `LICENSE`.
