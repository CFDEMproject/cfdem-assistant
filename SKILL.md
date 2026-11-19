---
name: cfdem-assistant
description: "Helps set up, debug, or extend OpenFOAM-based CFDEM(R) coupled CFD-DEM simulations (OpenFOAM with the Aspherix DEM solver via CFDEMcoupling): the CFD side and the coupling layer. Trigger when: working in a case directory with a CFD/ folder (constant/couplingProperties, system/decomposeParDict, system/controlDict) alongside a DEM/ folder with a .asx script; the user mentions cfdemSimulate, CFDEMcoupling, couplingProperties, forceModels, voidFractionModels or locateModels; or asks to build, run, extend the run time of, or debug a cfdemSolver* case. For a coupled case also load aspherix-assistant for the DEM/.asx side."
---

# Context

You are an assistant that will help with the setup of OpenFOAM-based CFDEM(R) solvers — simulations that couple OpenFOAM CFD with the Aspherix(R) DEM solver.

This skill targets **OpenFOAM 10** exclusively — the only OpenFOAM version the current CFDEM coupling supports.
Never introduce syntax, defaults, or directory conventions from another OpenFOAM version (ESI/OpenCFD releases, or other Foundation versions) without checking it applies to OpenFOAM 10 too.

This skill complements [Aspherix Assistant](https://github.com/CFDEMproject/aspherix-assistant) (a sibling skill).
Aspherix Assistant covers the DEM side of a coupled case (the `.asx` input script); this skill covers the CFD side and the coupling layer itself (the OpenFOAM case, the coupling dictionaries, and how the two solvers are wired together).
For a coupled case, expect both skills to be active.

# Startup

Before doing anything else, check whether this skill's own repository (the directory containing this `SKILL.md`) is behind its upstream — the rules and guidance below may be stale otherwise.
Run this from that directory, not the case/working directory you'll build the simulation in:
```
git fetch --quiet && git status -uno
```
If it's not a git repository (e.g. it was copied rather than cloned), skip this check silently — don't error or warn about it.
If it reports being behind, tell the user how many commits and offer to pull — don't pull automatically, since it could change this skill's own instructions mid-session.

# Resources

## CFDEM notes shipped with the code (read these first)

The notes on the CFDEM tools and models — rules every case must follow, the CFDEM environment, solver choice and gotchas, `couplingProperties`, model keywords, `cfdemSimulate`, and coupling-specific debugging strategies — live in the CFDEMcoupling repository, as `.. ai-note::` blocks in the reference pages (`documentation/coupling/src/`).
In the built documentation they are HTML comments (`<!-- AI-NOTE ... -->`): not rendered in a browser, but in the page source of the installed documentation, so they match the installed version.
They are deliberately not copied into this skill.
Plain HTML-to-text readers and fetch tools drop comments, so read them with the script:

```
scripts/ai_notes.py                  # the notes of all pages (start here)
scripts/ai_notes.py cfdemSimulate    # the notes of the named pages, .html optional
```

Run it without arguments once before touching any case: the first block (`Section_gettingStarted`) holds the rules every case must follow, the others are keyed by the page they belong to.
`scripts/fetch_section.py` appends the notes of the page it reads, so a page read through it brings its notes along.
The script resolves the documentation like the other scripts (`--docs online|<path>`, exit code 3 = ask the user, see `references/CFDEM_DOC_SEARCH.md`); without page names it needs a local documentation directory (`online` has no page list).
Pages not enabled by the licence are replaced by a placeholder in the installed documentation and carry no notes: that is normal.
If it reports `AI_NOTES_NOT_FOUND`, the install predates the notes: tell the user, and fall back to the reference pages below.

**Before running, compiling or inspecting anything, make sure the CFDEM environment is loaded**: `echo $CFDEM_PROJECT_DIR`; if empty, `source <install>/etc/bashrc` (`etc/zshrc` on zsh) of the CFDEMcoupling install.
`aspherix` missing from `PATH` usually means the environment is not loaded, not that Aspherix is missing; the notes are found via `$CFDEM_ASX_EXEC` once it is.
Details are in the notes of `environmentVars`.

## CFDEM reference documentation

The CFDEM(R)/CFDEMcoupling reference pages (syntax, keywords, defaults, model lists) are a Sphinx + Read the Docs site shared with the Aspherix documentation.
`references/CFDEM_DOC_SEARCH.md` says how to find and fetch the right page from the installed documentation.

## OpenFOAM baseline

OpenFOAM itself is well represented in model training data — don't re-derive or dump dictionary syntax that's already reliable general knowledge.
See `references/OPENFOAM.md` for the short list of official documentation links to verify a specific detail (a dictionary key, a boundary condition type, a solver flag).

## OpenFOAM utility guidance

Per-command guidance, one file per command, for inspecting or debugging a case:

- `foamDictionary`: `references/commands/foamDictionary.md`
- `checkMesh`: `references/commands/checkMesh.md`
- `foamListTimes`: `references/commands/foamListTimes.md`
- `postProcess`: `references/commands/postProcess.md`
- `foamLog`: `references/commands/foamLog.md`
- `decomposePar`: `references/commands/decomposePar.md`
- `reconstructPar`: `references/commands/reconstructPar.md`

## General strategies

`references/strategies/STRATEGIES.md` holds problem-solving strategies that do not depend on the CFDEM version (validation, comparison, meshing); the coupling-specific ones are in the notes' `strategies.md`.
