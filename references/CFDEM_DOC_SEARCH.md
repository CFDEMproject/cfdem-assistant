# Searching the CFDEM Coupling Documentation

The CFDEM(R)/CFDEMcoupling documentation ([website](https://doc.aspherix-dem.com/coupling/), [index](https://doc.aspherix-dem.com/coupling/genindex.html)) is a static Sphinx + Read the Docs site, the same as the public Aspherix documentation — it's a sibling section of the same site (`coupling/` alongside `main/`, `solver/`, `gui/`, `calibration/`).
The search strategy below mirrors Aspherix Assistant's own `DOC_SEARCH.md` exactly; only the base path differs.

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

## Page structure

Model/command/solver pages follow a consistent Sphinx layout, so name the section you need instead of asking for the whole page.
All real content lives inside `<section id="...">` blocks; everything outside them (sidebar nav, footer, prev/next links) is boilerplate and can be ignored.
The recurring sections, in order, are: the title section (entity name), `#syntax` (dictionary keys/arguments — absent on some solver pages, which go straight to `#description`), `#examples`, `#description` (semantics), `#literature` (citation for the underlying method, common on force/void-fraction models), `#restrictions`, `#related-commands`.
For a syntax/keys question, ask for `Syntax`; for "how does this model work" questions, ask for `Description` (and `Literature` if you need the source); for a working snippet, ask for `Examples`.

## Fetching a page

Once you've resolved the exact page and section name (above), escalate through these three strategies in order — stop at the first one that gives you a complete, accurate answer.

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
scripts/fetch_section.py <url> <section-id>
```

and returns only the extracted text. `scripts/fetch_section.py <url> --list` prints every section id on a page first, if you're not sure of the exact id (see "Page structure" above for how ids map to the recurring section names).
This is a plain HTML→text extraction with no model involved anywhere in the fetch — the precision backstop when Strategy 1's summarization isn't good enough.
Running it in a subagent, rather than inline, keeps the raw HTML and script output out of your own context window; only the clean extracted text comes back.

### Strategy 3: run `scripts/fetch_section.py` yourself

If the harness has no way to spawn a subagent at all, run the same script directly instead — same command, same output as Strategy 2, just accepting that the output lands in your own context since there's no alternative.
