# Searching the CFDEM Coupling Documentation

The CFDEM(R)/CFDEMcoupling documentation ([website](https://doc.aspherix-dem.com/coupling/), [index](https://doc.aspherix-dem.com/coupling/genindex.html)) is a static Sphinx + Read the Docs site, the same as the public Aspherix documentation — it's a sibling section of the same site (`coupling/` alongside `main/`, `solver/`, `gui/`, `calibration/`).
The search strategy below mirrors Aspherix Assistant's own `DOC_SEARCH.md` exactly; only the base path differs.

## Which documentation to read

By default the scripts read the documentation of the **installed Aspherix/CFDEM**: `<install>/documentation/coupling/`, found relative to the `aspherix` binary on `PATH`. It matches the installed version; the website always shows the latest release, so its pages, section layout, keywords and licence-gated entries can differ (the public site may lag behind the monorepo's current docs).
`scripts/doc_index.py` and `scripts/fetch_section.py` say which source they use on stderr (`# Using ...`); mention it to the user when it matters. `fetch_section.py` takes the website URL (or `coupling/<page>.html`) and maps it to the source in use.

An explicit choice overrides the default: `--docs online` (the website) or `--docs <path>` (a local documentation directory containing `coupling/`, e.g. a monorepo build `documentation/build/html`) on either script, or the same value in `$ASPHERIX_DOC_BASE`. A source named by the user or in the project's `CLAUDE.md` counts as explicit: pass it with `--docs` on every call (shell state doesn't persist between calls).

If there is no explicit choice and no `aspherix` binary (or no docs next to it), the scripts print `DOCS_SOURCE_UNRESOLVED` and exit with code 3, without guessing. They can't prompt, so **ask the user** whether to use the online docs (latest release; version or licence-enabled features may differ) or a local documentation directory, then re-run with `--docs` and remember the answer for the conversation.
A fetch tool (WebFetch etc.) only reaches the website, so for version-exact answers skip "Strategy 1" below and use the scripts.
A page missing from the installed docs is reported as not found: it may be newer than the install, or not enabled by the licence. The scripts don't fall back to the website on their own.
The layout notes below (section ids, keyword rendering) describe the current docs; against older docs run `fetch_section.py <url> --list` first and don't assume them.

## Finding the right page

Pages are named after the entity they document: `https://doc.aspherix-dem.com/coupling/<entityName>.html`.
Solvers are named directly (`cfdemSolverPiso.html`, `cfdemSolverPimple.html`), sub-models are prefixed by their model family (`forceModel_DiFeliceDrag.html`, `voidFractionModel_IBVoidFraction.html`, `IOModel_basicIO.html`).
A `List_<modelFamily>.html` page (e.g. `List_forceModels.html`) enumerates every model in that family — use it to discover what exists before guessing a name.
If you already know the entity name, construct this URL directly instead of searching first.

## Using the object inventory

If the exact entity name isn't known, use `objects.inv` — the site's Sphinx object inventory — as the authoritative index of every documented page, rather than crawling `genindex.html` or pulling whole pages into a scratch file to find the right one.
It's a zlib-compressed binary file, not HTML, so a URL-fetching tool that expects renderable content (e.g. Claude Code's WebFetch) can't parse it directly; use `scripts/doc_index.py` (in this skill's own repo) to fetch and decompress it instead of reaching for inline `curl`/`python3 -c`:

```
scripts/doc_index.py                # full inventory
scripts/doc_index.py forceModel     # only entries whose name/displayname contains "forceModel"
```

Each line is `name domain:role priority uri displayname`.
`std:doc` entries are full pages (`uri` is the page's `.html` filename); `std:confval`/`std:envvar` entries are settings/environment-variable anchors within a page, not standalone pages.

**Per-model keywords are not in `objects.inv`.** The options of an individual model (`alphaMin`, `maxCellsPerParticle`, …) are documented with `.. keyword::`, which is deliberately not registered in the inventory so the same name can appear on many pages; `doc_index.py <keyword>` therefore finds nothing (only global `couplingProperties` settings are `std:confval` entries).
To locate a keyword, find the model page (by model name via `doc_index.py`/`List_<family>.html`) and read its `keywords-options` section, or `grep -rn "keyword:: <name>" documentation/coupling/src` in the monorepo.

Some families have a landing page of a different shape than `List_<family>.html`: solvers and utilities are `Section_solvers.html` / `Section_utilities.html`, and the finite-volume extensions are `List_finiteVolumeExtensions.html`, whose entries are `fvConstraints_<name>.html` / `fvModels_<name>.html` (the former `fvOptions_*` pages no longer exist).

## Page structure

Model/command/solver pages follow a consistent Sphinx layout, so name the section you need instead of asking for the whole page.
All real content lives inside `<section id="...">` blocks; everything outside them (sidebar nav, footer, prev/next links) is boilerplate and can be ignored.
Model pages (`forceModel_*`, `voidFractionModel_*`, …) have these sections, in order, with these ids: the title section (id is the lowercased model name, e.g. `difelicedrag`), `#description` (semantics), `#syntax` (the dictionary it lives in plus a working example snippet — there is no separate `#examples` section), `#keywords-options` (every model-specific keyword, see below), `#restrictions` (optional), `#related-commands`, `#literature` (citation for the underlying method, optional, common on force/void-fraction models). Solver and utility pages may lack `#syntax`/`#keywords-options` and go straight to `#description`.
For a "which keys does this model take" question, ask for `keywords-options` (plus `syntax` for the example); for "how does this model work", ask for `description` (and `literature` for the source). Use `scripts/fetch_section.py <url> --list` if unsure of an id.

In `keywords-options` each keyword is one line `name type default: <value> | mandatory | optional`, followed by its indented description. A keyword indented below another one only applies in the context of that parent. Titled groups ("Thermal properties", "Fluid fields & interpolation", …) appear as plain title lines above their keywords. `fetch_section.py` already renders this structure (it drops the web page's "… more"/"less" toggles).

## Fetching a page

Once you've resolved the exact page and section name (above), escalate through these three strategies in order — stop at the first one that gives you a complete, accurate answer.

A page listed in `List_<family>.html` or `objects.inv` that "404s" is not a dead link — it means that entity is withheld from this licence/distribution (some models and solvers are gated).
On the website this is a *soft* 404: the request returns HTTP 200, with a page body reading "*The page you requested cannot be found. Most likely this is because the particular feature is not enabled by your license.*" — checking the HTTP status code alone won't catch it; `scripts/fetch_section.py <url> --list` on such a page returns a single `not-found` section id, which is the reliable way to detect it.
Don't spend a fetch-strategy escalation trying to recover a page that 404s this way; note the gap and, if the model is actually needed, fall back to the CFDEMcoupling source tree (`src/lagrangian/cfdemParticle/subModels/<family>/`) instead.

### Strategy 1: a fetch tool, with a verbatim-constrained prompt

Most coding-agent harnesses (Claude Code's WebFetch, Gemini CLI's web_fetch, etc.) fetch a URL through a small model that only sees the URL and the prompt you give it — it can't browse or search the site itself, starts with no context on CFDEM coupling or this skill, and, being small, tends to summarize or paraphrase dense reference content (a `couplingProperties`-style settings list, a `List_<family>.html` model enumeration) rather than reproducing it exactly.
Counter that directly in the prompt:

- Name exactly what to extract (e.g. "the settings under `Model and parameter settings` on the `couplingProperties` page"), not an open-ended "summarize this page".
- Tell it not to paraphrase: *"reproduce the exact key names, types, and defaults verbatim — do not summarize, paraphrase, or omit any entry."*
- For tabular/enumerated content, ask for a markdown table with named columns rather than prose — a table forces per-row enumeration instead of compression.

If the result still looks incomplete (a setting you expected is missing, or you got prose where you asked for a table), retry the same URL with an even narrower prompt scoped to a single key before moving to Strategy 2 — most such tools cache by URL for a short window, so repeat asks against the same page are cheap.

### Strategy 2: a subagent runs `scripts/fetch_section.py`

When Strategy 1 is unavailable, or still isn't reliable enough for content where exact fidelity matters, and the harness supports spawning a subagent for a tool call (e.g. Claude Code's `Agent` tool), delegate the fetch to one rather than running it yourself.
The subagent runs:

```
scripts/fetch_section.py [--docs online|<path>] <url> <section-id>
```

and returns only the extracted text. `scripts/fetch_section.py <url> --list` prints every section id on a page first, if you're not sure of the exact id (see "Page structure" above for how ids map to the recurring section names).
This is a plain HTML→text extraction with no model involved anywhere in the fetch — the precision backstop when Strategy 1's summarization isn't good enough.
Running it in a subagent, rather than inline, keeps the raw HTML and script output out of your own context window; only the clean extracted text comes back.

### Strategy 3: run `scripts/fetch_section.py` yourself

If the harness has no way to spawn a subagent at all, run the same script directly instead — same command, same output as Strategy 2, just accepting that the output lands in your own context since there's no alternative.
