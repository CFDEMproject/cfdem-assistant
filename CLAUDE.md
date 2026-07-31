# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This file provides guidance to Claude Code when working *on* this repository — i.e. when developing, extending, or maintaining the CFDEM Assistant skill itself.
It is not part of the skill's own content and is never loaded by a harness using the skill: an agent running CFDEM Assistant to build a case only sees `SKILL.md` and `references/`, never this file.
If you're looking for the skill's actual instructions/content, start at `SKILL.md` instead.

## What this repository is

This repo defines a Claude Code **skill** named "CFDEM Assistant" — it is not an application with source code, build steps, or tests.
It helps with the setup of OpenFOAM-based CFDEM(R) solvers: simulations that couple OpenFOAM CFD with a DEM particle solver (LIGGGHTS/Aspherix(R)).

The skill targets **OpenFOAM 10** exclusively — not a preference, but the only OpenFOAM version the current CFDEM coupling is compatible with.
Any OpenFOAM guidance added here (rules, commands, links) must be OpenFOAM-10-specific; don't generalize across OpenFOAM versions.

This skill is a companion to the sibling **Aspherix Assistant** skill (`/home/dll/DCS/Agents/AspherixAssistant`).
Aspherix Assistant covers the DEM side of a coupled case (the `.asx`/LIGGGHTS input script); this skill covers the CFD side and the coupling layer (the OpenFOAM case, the coupling dictionaries, and how the two solvers are wired together).
Keep that division of responsibility — don't duplicate DEM-side rules here; link to Aspherix Assistant's content instead of forking it.

- `SKILL.md` — the skill definition (frontmatter + instructions loaded when the skill is invoked).
- `references/RULES.md` — the single source of truth for rule *content* that applies to every CFDEM-coupled case built with this skill.
  The rule text itself must live only in `references/RULES.md` — don't fork rule content into multiple places.
- `references/OPENFOAM.md` — links to *official* OpenFOAM documentation, used to verify specifics rather than to teach OpenFOAM from scratch.
  Deliberately thin: see "OpenFOAM content stays thin" below.
- `references/commands/<name>.md` — per-command guidance, one file per command worth documenting beyond the public docs.
- `references/dictionaries/<name>.md` — per-dictionary reference for a CFDEM coupling dictionary (e.g. `couplingProperties`), one file per dictionary worth documenting beyond the public docs.
  Unlike `references/OPENFOAM.md`, these are *not* kept thin — CFDEM coupling content isn't in model training data, so a full, accurate reference genuinely earns its keep here. Source it from `references/CFDEM_DOC_SEARCH.md`'s local docs, not from recall or fabrication.
- `references/strategies/STRATEGIES.md` — short, self-contained problem-solving strategies.
  A strategy that needs its own examples or multi-step walkthrough gets its own `references/strategies/<name>.md` file, linked from `STRATEGIES.md`.

## OpenFOAM content stays thin

OpenFOAM's dictionaries, solvers, and boundary conditions are common enough that model training data already covers them reliably.
Do not build a general-purpose OpenFOAM reference in this repo (dictionary dumps, BC catalogues, solver-selection tables) — that duplicates what models already know and rots as OpenFOAM versions change.
`references/OPENFOAM.md` should stay a short list of links to authoritative docs, used to verify a specific detail, not a teaching document.

This is about *content* — dictionary keys, BC types, solver selection tables — not about *utility* usage.
Per-utility CLI guidance (`foamDictionary`, `checkMesh`, `foamListTimes`, `postProcess`, `foamLog`, …) belongs in `references/commands/<name>.md`, the same as Aspherix Assistant documents its own commands: these are operational recipes for using a specific tool well (which flags, when, what the output means, what's destructive), not a re-teaching of OpenFOAM concepts.

Two existing public skills were pulled down and inspected while scoping this repo (not vendored here — for reference only).
`hpc-openfoam` from [SciMate-AI/HPC-Skills](https://github.com/SciMate-AI/HPC-Skills) uses a progressive-disclosure structure similar to this repo's.
`openfoam-cfd` from [Soljourner/claude-engineering-skills](https://github.com/Soljourner/claude-engineering-skills) inlines a large monolithic dictionary/BC reference into one `SKILL.md`.
Neither addresses CFDEM/DEM particle coupling — that's the actual gap this skill fills.
Don't imitate the monolithic-dictionary-dump style; follow the progressive-disclosure style instead (see "Working in this repo" below).

## CFDEM coupling documentation is local for now, not public

CFDEMcoupling's own documentation is not public yet, but it does exist: a static Sphinx-generated site bundled with the Aspherix installation at `$ASX_INSTALL/documentation/coupling/`.
`references/CFDEM_DOC_SEARCH.md` documents how to search and read it — deliberately written the same way as Aspherix Assistant's public-docs search strategy (name-based page lookup, `objects.inv` as the index, section-scoped reads), so that when DCS publishes this documentation online, only the location and fetch mechanism (local file read vs. `WebFetch`) need to change, not the strategy itself.
Do not search the public web for CFDEM/CFDEMcoupling docs — there's no public source to find yet — and do not fabricate CFDEM-specific syntax or defaults from general CFD knowledge; verify against the local docs or internal material, or ask.

## Commit messages

Every commit made by an AI agent must end with a `Co-Authored-By:` trailer naming the specific model that wrote it (e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`), not a generic tool name.
This repo relies on that trailer to audit which model authored which change, so use the exact model name/version, and never omit or genericize it.

## Markdown formatting

Do not hard-wrap prose lines in this repo's markdown files.
Use one sentence per line instead: each sentence gets its own line, with no manual mid-sentence line breaks.
Let the rendering editor/viewer soft-wrap sentences that exceed the display width.
This applies to prose paragraphs only — code blocks, tables, and lists are unaffected.
This matches the convention already used in the sibling Aspherix Assistant repo.

## Working in this repo

- When adding or changing a rule that CFDEM cases must follow, edit `references/RULES.md` directly rather than duplicating rule text elsewhere.
- When adding guidance specific to one command, put it in its own `references/commands/<name>.md` file and link it from `SKILL.md`'s Guidelines section, rather than growing `references/RULES.md` or `SKILL.md` itself.
- When adding a problem-solving strategy: a short one goes directly in `references/strategies/STRATEGIES.md`; a strategy that needs its own examples or walkthrough gets its own `references/strategies/<name>.md` file, linked from `STRATEGIES.md`.
- When a rule or piece of guidance belongs to the DEM side of a coupled case, point to Aspherix Assistant instead of writing it here.
