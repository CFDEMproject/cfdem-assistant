# smoothingModels

Source: [`smoothingModel.html`](https://doc.aspherix-dem.com/coupling/smoothingModel.html), [`List_smoothingModels.html`](https://doc.aspherix-dem.com/coupling/List_smoothingModels.html) — see `references/CFDEM_DOC_SEARCH.md` to look up an individual model's own page.

## The `smoothingModel` command

Selected in `couplingProperties`:

```
smoothingModel model;
```

No default — must be set explicitly.
A smoothing model smooths the exchange fields between CFD and DEM: the voidfraction field, and the `Ksl` field in the case of implicit force coupling (see `treatForceExplicit` in `references/models/forceModels.md`).
This matters when particles are larger than the local cell size — without smoothing, the exchange fields can develop sharp, unphysical gradients at the particle/cell scale rather than varying smoothly across the domain.

## Available smoothing models

`constDiffSmoothing`, `noSmoothing` (no-op — use when particles are small relative to the cell size and smoothing isn't needed), `particleSizeDiffSmoothing`.

Check `List_smoothingModels.html` (via `references/CFDEM_DOC_SEARCH.md`) for the current authoritative list before picking one — this list can drift from the live docs over time.
