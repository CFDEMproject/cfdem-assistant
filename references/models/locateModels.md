# locateModels

Source: [`locateModel.html`](https://doc.aspherix-dem.com/coupling/locateModel.html), [`List_locateModels.html`](https://doc.aspherix-dem.com/coupling/List_locateModels.html) — see `references/CFDEM_DOC_SEARCH.md` to look up an individual model's own page.

## The `locateModel` command

Selected in `couplingProperties`:

```
locateModel model;
```

No default — must be set explicitly.
A locate model maps each Lagrangian (DEM) particle position to the Eulerian CFD cell (and cell ID) it's currently in — the basic per-timestep lookup that every void-fraction/force calculation depends on.
Always paired with a `voidFractionModel` choice; the two are usually chosen together (an IB-style locate model pairs with an IB-style void-fraction model, and so on) — see `references/models/voidFractionModels.md` and `references/dictionaries/couplingProperties.md`.

## Available locate models

**The dictionary keyword often differs from the doc-page/class name below** — always check the model's own `#syntax` section rather than assuming the class name is the literal value to write in `couplingProperties`.

| Class / doc page | `couplingProperties` keyword | Notes |
|---|---|---|
| `engineSearch` | `engine` | Default-recommended general-purpose model; walk algorithm from the last known cell, falling back to a linear (`treeSearch false`) or recursive tree (`treeSearch true`, recommended) search. |
| `engineSearchIB` | `engineIB` | Modification of `engine` for parallel immersed-boundary solvers: adds satellite points on the particle surface so (parts of) a sphere can still be located when its centre has moved to another processor. Only for IB solvers. |
| `engineSearchIBBoxSimple` | — | Listed in `List_locateModels.html` and `objects.inv`, but its doc page (`locateModel_engineSearchIBboxSimple.html`) is a soft 404 (HTTP 200, "not enabled by your license" body) on the live site — this model is withheld from the public docs (licence/distribution-restricted), not a broken link. See `references/CFDEM_DOC_SEARCH.md` for how to recognize this. Its keyword/syntax aren't publicly documented; grep the CFDEMcoupling source (`subModels/locateModel/`) if this one is actually needed. |
| `engineSearchSuperquadric` | `engine` (same keyword as plain `engineSearch`; distinguished by `particleShapeType superquadric` in the same dictionary) | Same satellite-point idea as `engineSearchIB`, applied to superquadric particle surfaces instead of spheres. Requires `particleShapeType superquadric` *and* a force model that supports that shape type. Only for IB solvers with superquadric particles. |
| `standardSearch` | `standard` | The "very straightforward (robust!)" fallback — a plain per-step search with no seed-cell/tree optimization. No IB restriction, no extra props beyond `writeProcHistogram`. |
| `turboEngineSearch` | `turboEngine` | `engineSearch` derivative tuned for better parallel performance (bounding-box info, seed-cell walk). Has an `allowParticlesOutsideCFDdomain` switch worth knowing about whenever the DEM domain is deliberately larger than the CFD domain (a common pattern for insertion-zone buffers, see e.g. the `harvester` use case) — leaving it at its default `false` triggers an expensive strict fallback search for every DEM position outside the fluid domain, every step. |

Check `List_locateModels.html` (via `references/CFDEM_DOC_SEARCH.md`) for the current authoritative list before picking one — this list can drift from the live docs over time.

## Common properties

Every model above accepts `writeProcHistogram` (switch, default `false`) in its own `<keyword>Props` sub-dict — write, per processor and globally, how many particles were located in the CFD mesh. Most also accept `treeSearch` (switch, default `true` for `engineSearch`/`engineSearchIB`/`turboEngineSearch`) toggling the tree-search fallback described per-model above; `standardSearch` has neither seed-cell nor tree-search behavior, so it doesn't expose this switch.

## IB-specific settings

`engineSearchIB` adds `zSplit` (default `8`, number of z-normal satellite-point layers) and `xySplit` (default `16`, satellite points per layer). `engineSearchSuperquadric` exposes the same two keys but with no documented default — set them explicitly for that model.
