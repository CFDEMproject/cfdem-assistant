# voidFractionModels

Source: [`voidfractionModel.html`](https://doc.aspherix-dem.com/coupling/voidfractionModel.html), [`List_voidFractionModels.html`](https://doc.aspherix-dem.com/coupling/List_voidFractionModels.html) — see `references/CFDEM_DOC_SEARCH.md` to look up an individual model's own page.

## The `voidfractionModel` command

Selected in `couplingProperties`:

```
voidfractionModel model;
```

No default — must be set explicitly.
A void-fraction model computes the voidfraction in each CFD cell — the ratio of empty (fluid) volume to total cell volume, i.e. `1 - (total particle volume in the cell / cell volume)`.
It's the base class for every model representing a DEM particle's volume in the CFD domain as a voidfraction field; the choice of model determines how that particle-to-cell mapping is done (e.g. point-centre vs. divided/distributed across neighboring cells vs. immersed-boundary-style).

## Available void-fraction models

`IBVoidFraction`, `IBVoidFractionConvex`, `IBVoidFractionSuperquadric`, `bigParticleVoidFraction`, `centreVoidFraction`, `dividedVoidFraction`, `dividedMPVoidFraction`, `dividedVoidFractionSuperquadric`, `hybridVoidFraction`, `noVoidFraction`, `testVoidFraction`, `tetBasedVoidFraction`, `weightedNeigbhorsVoidFraction`.

Check `List_voidFractionModels.html` (via `references/CFDEM_DOC_SEARCH.md`) for the current authoritative list before picking one — this list can drift from the live docs over time.
The `IB*` variants pair with an immersed-boundary-style `locateModel`; the `divided*` variants distribute a particle's volume across the cells it overlaps rather than assigning it entirely to one cell — relevant when particles are comparable in size to, or larger than, the local cell size.

## `useDDTvoidfraction` masking

`couplingProperties`' `useDDTvoidfraction` setting (see `references/dictionaries/couplingProperties.md`) enables the time-derivative-of-voidfraction term.
When enabled, a region can be excluded from that `ddt(voidfraction)` term via a `maskingRegion` sub-dictionary inside the chosen void-fraction model's own properties dictionary:

```
<voidfractionModel>Props
{
    ddtVoidfractionProps
    {
        maskingRegion
        {
            type <regionType>;
            name <regionName>;
        }
    }
}
```

- `type` — `cellZone` to exclude a named cell zone, or `none` (default) to exclude nothing.
- `name` — the region name (the `cellZone` name); required only when `type` is `cellZone`.

Example:

```
dividedProps
{
    ddtVoidfractionProps
    {
        maskingRegion
        {
            type cellZone;
            name excludedCellZone;
        }
    }
}
```
