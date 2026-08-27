# postProcessingModels

Source: [`postProcessingModel_checkCouplingInterval.html`](https://doc.aspherix-dem.com/coupling/postProcessingModel_checkCouplingInterval.html), [`List_postProcessingModels.html`](https://doc.aspherix-dem.com/coupling/List_postProcessingModels.html), and the ["Diagnose coupling stability and accuracy issues" how-to](https://doc.aspherix-dem.com/coupling/Section_how_to.html) — see `references/CFDEM_DOC_SEARCH.md` to look up a page yourself.

## The `postProcessingModels` command

Selected in `couplingProperties`:

```
postProcessingModels
(
    model_x
    model_y
);
```

Default: `checkCouplingInterval` and `checkFluxBalance` (see `references/dictionaries/couplingProperties.md`).
If a case needs an additional model (e.g. `fieldStore`), append it to the default list rather than replacing it, unless there's a specific reason to drop one of the defaults.

## `checkCouplingInterval`

On by default whenever particles are present, but silent by default. See the how-to link above for what it checks and how to make it visible (`checkCouplingIntervalProps { silent false; }`).

## `checkFluxBalance`

The other default post-processing model; checks mass/flux consistency between the CFD and DEM sides. See [`postProcessingModel_checkFluxBalance.html`](https://doc.aspherix-dem.com/coupling/postProcessingModel_checkFluxBalance.html) for details.
