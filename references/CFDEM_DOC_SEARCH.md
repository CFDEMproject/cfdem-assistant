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
It's a zlib-compressed binary file, not HTML, so a URL-fetching tool that expects renderable content (e.g. Claude Code's WebFetch) can't parse it directly; fetch and decompress it with a shell command instead:

```
curl -s https://doc.aspherix-dem.com/coupling/objects.inv -o /tmp/objects.inv
python3 -c "import zlib; d=open('/tmp/objects.inv','rb').read(); print(zlib.decompress(d.split(b'\n',4)[4]).decode())"
```

Each line is `name domain:role priority uri displayname`.
`std:doc` entries are full pages (`uri` is the page's `.html` filename); `std:confval`/`std:envvar` entries are settings/environment-variable anchors within a page, not standalone pages.

## Page structure

Model/command/solver pages follow a consistent Sphinx layout, so name the section you need instead of asking for the whole page.
All real content lives inside `<section id="...">` blocks; everything outside them (sidebar nav, footer, prev/next links) is boilerplate and can be ignored.
The recurring sections, in order, are: the title section (entity name), `#syntax` (dictionary keys/arguments — absent on some solver pages, which go straight to `#description`), `#examples`, `#description` (semantics), `#literature` (citation for the underlying method, common on force/void-fraction models), `#restrictions`, `#related-commands`.
For a syntax/keys question, ask for `Syntax`; for "how does this model work" questions, ask for `Description` (and `Literature` if you need the source); for a working snippet, ask for `Examples`.

## Fetching a page

Most coding-agent harnesses (Claude Code's WebFetch, Gemini CLI's web_fetch, etc.) fetch a URL through a small subagent that only sees the URL and the prompt you give it — it can't browse or search the site itself, and it starts with no context on CFDEM coupling or this skill.
Once you've resolved the exact page (above), pass that URL with a narrow, specific prompt naming exactly what to extract (e.g. "list every setting under `Model and parameter settings` for the `couplingProperties` page, with defaults and types"), not an open-ended "summarize this page".
A vague prompt on a large reference page tends to make the subagent return either too little (missing a setting you needed) or the whole page verbatim — which is how full pages end up dumped into scratch files instead of just the answer.

If the harness has no such fetch tool at all, `curl` the page and extract the relevant section directly (e.g. `curl -s <url> | lynx -dump -stdin` or similar) rather than dumping the raw HTML into context or a scratch file.
