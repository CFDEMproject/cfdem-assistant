# Searching the CFDEM Coupling Documentation

The CFDEM(R)/CFDEMcoupling documentation is not public yet.
Until it is, use the local copy that ships with the Aspherix installation instead: a static Sphinx-generated site at `$ASX_INSTALL/documentation/coupling/` (check the `ASX_INSTALL` environment variable for the path; ask the user if it isn't set).
It's the same Sphinx/Read-the-Docs structure as the public Aspherix documentation, so the search strategy below mirrors Aspherix Assistant's `DOC_SEARCH.md` — only the location and fetch mechanism differ (local files, not a URL).

Once DCS publishes this documentation online, replace the local path below with the real URL and switch page reads from `Read`/local file access to `WebFetch`; the page-resolution strategy (name-based lookup, `objects.inv`, section-scoped reads) stays the same.

## Finding the right page

Pages are named after the entity they document: `<entityName>.html`.
Solvers are named directly (`cfdemSolverPiso.html`, `cfdemSolverPimple.html`), sub-models are prefixed by their model family (`forceModel_DiFeliceDrag.html`, `voidFractionModel_IBVoidFraction.html`, `IOModel_basicIO.html`).
A `List_<modelFamily>.html` page (e.g. `List_forceModels.html`) enumerates every model in that family — use it to discover what exists before guessing a name.
If you already know the entity name, construct the path directly instead of searching first.

## Using the object inventory

If the exact entity name isn't known, use `objects.inv` (in the same directory) as the authoritative index of every documented page, rather than crawling `genindex.html` or reading whole pages to find the right one.
It's zlib-compressed, not HTML, so decompress it with a shell command instead of trying to read it directly:

```
python3 -c "import zlib; d=open('$ASX_INSTALL/documentation/coupling/objects.inv','rb').read(); print(zlib.decompress(d.split(b'\n',4)[4]).decode())"
```

Each line is `name domain:role priority uri displayname`.
`std:doc` entries are full pages (`uri` is the page's `.html` filename); `std:confval`/`std:envvar` entries are settings/environment-variable anchors within a page, not standalone pages.

## Page structure

Model/command pages follow a consistent layout, so read the section you need instead of the whole page.
The recurring sections, in order, are: the title section (entity name), `#syntax` (dictionary keys/arguments — absent on some solver pages, which go straight to `#description`), `#examples`, `#description` (semantics), `#literature` (citation for the underlying method, common on force/void-fraction models), `#restrictions`, `#related-commands`.
For a syntax/keys question, ask for `#syntax`; for "how does this model work" questions, ask for `#description` (and `#literature` if you need the source); for a working snippet, ask for `#examples`.

## Reading a page

Since the docs are local HTML files for now, read them directly rather than fetching a URL.
Extract just the section you need (e.g. with a small script that strips tags from the relevant `<section id="...">` block, or `lynx -dump <file>` if available) instead of reading the raw HTML wholesale into context — the same reasoning as Aspherix Assistant's guidance against dumping full pages: a targeted read finds the answer, a full dump doesn't.
