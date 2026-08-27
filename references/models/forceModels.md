# forceModels (and forceSubModels)

Source: [`forceModel.html`](https://doc.aspherix-dem.com/coupling/forceModel.html), [`forceSubModel.html`](https://doc.aspherix-dem.com/coupling/forceSubModel.html), [`List_forceModels.html`](https://doc.aspherix-dem.com/coupling/List_forceModels.html) — see `references/CFDEM_DOC_SEARCH.md` to look up an individual model's own page.

## The `forceModel` command

Selected in `couplingProperties`:

```
forceModels
(
    model_x
    model_y
);
```

No default — must be set explicitly.
Each force model computes forces (e.g. fluid-particle interaction forces) acting on every DEM particle and every CFD cell.
All selected force models run sequentially each coupling step, and their forces are superposed — order in the list can matter for models that read fields another model writes.
If a fluid density field is needed, the field named `rho` is used by default; a `forceSubModel` can select an alternative field instead.
Not every force model computes an actual force — some exist only to produce additional output fields.

### Coarse graining restriction

Most force models support coarse graining.
If a force model that does *not* support coarse graining is used together with coarse graining, the simulation stops.
Set `cgWarnOnly true;` in `couplingProperties` to downgrade this to a warning printed to the log instead of a hard stop.

### Available force models

Drag: `Archimedes`, `ArchimedesIB`, `BeetstraDrag`, `BenyahiaDrag`, `DEMbasedDrag`, `DeereDrag`, `DiFeliceDrag`, `GidaspowDrag`, `HoelzerSommerfeldDrag`, `KochHillDrag`, `OzelSundaresanDrag`, `RongDrag`, `SchillerNaumannDrag`, `StokesClumpDrag`, `StokesSpheroidDrag`, `noDrag`.
Lift: `AutonLift`, `MeiLift`.
Immersed-boundary: `ArchimedesIB`, `ShirgaonkarIB`, `newIB`.
Lagrangian/Eulerian scalar & spray coupling: `LaEuFilmFormation`, `LaEuFilmFormationSpray`, `LaEuForcingHFDIBM`, `LaEuScalarCapture`, `LaEuScalarDust`, `LaEuScalarEmit`, `LaEuScalarLiquid`, `LaEuScalarMass`, `LaEuScalarRadiation`, `LaEuScalarSpray`, `LaEuScalarTemp`, `LaEuScalarTempIB`.
Other physics: `electrostaticForce`, `evaporateThermal`, `gradPForce`, `interface`, `liquidSurfaceReflection`, `melting`, `periodicPressure`, `rotorZoneMomentumSource`, `scalarGeneralExchange`, `scalarGeneralExchangePhaseChange`, `transferFields`, `transferTurbulence`, `transferVapour`, `turbulenceSlipInduced`, `virtualMassForce`, `viscForce`.

Check `List_forceModels.html` (via `references/CFDEM_DOC_SEARCH.md`) for the current authoritative list before picking one — this list can drift from the live docs over time.

## `forceSubModel`

A `forceSubModel` extends a `forceModel`: it handles the implicit/explicit force split and holds settings for that force model.
Defined as a sub-dictionary inside the owning `<forceModel>Props` dictionary:

```
<forceModel>Props
{
    forceSubModels
    (
        model_x
    );
}
```

If `forceSubModels` isn't given, `ImEx` is loaded by default — so explicitly listing `ImEx` alone changes nothing.

Available: `ImEx` (default), `ImExCorr`, `ImExDipole`, `ImExFibre`, `scaleDragByFieldFunction`, `scaleDragByReFunction`, `stochasticDispersion`, `superficialVelocity`, `twoParameterAutoDraG`, `twoParameterCorrection`, `voidageCorr`.

### Common switches

Availability depends on the specific `forceModel`; defaults are generally `false` unless a specific force model overrides that.

- `treatForceExplicit` — if `false` (default), the coupling force is treated semi-implicitly (drag coefficient × relative velocity between average particle velocity and local fluid velocity) — generally more stable. If `true`, the force is applied directly (explicit).
- `treatForceDEM` — if `false`, forces are calculated for both DEM and CFD; restrict to DEM-only with `true`.
- `implForceDEM` — if `true`, fluid velocity and drag coefficient are sent to the DEM side each coupling step and the drag force is computed there using the particle velocity (generally more stable, since drag decreases as the particle approaches the fluid velocity). If `false`, the CFD-computed drag force is used directly and held constant for one coupling interval. Support isn't guaranteed identical across `particleShapeType`s — verify it actually affects the result for the shape in use before trusting it, especially the first time it's combined with a given shape.
- `verbose` — print verbose output to screen.
- `interpolation` — if `true`, interpolate Eulerian field values to the particle position for the Lagrangian calculation; if `false` (default), use the cell-centre value.
- `useFilteredDragModel` — use a coarse-grid version of the Beetstra drag model that accounts for grid-size effects.
- `useParcelSizeDependentFilteredDrag` — coarse-grid Beetstra variant accounting for parcel-size effects; forces `useFilteredDragModel` to `true`.
- `scalarViscosity` — if `true`, read viscosity `nu` from the defining force model's own properties sub-dict for the drag calculation, instead of always using the value from `transportProperties` (which the momentum equation itself always uses regardless of this switch).
- `useCorrectedVoidage` — use corrected voidfraction.
- `anisotropicDrag` — use anisotropic drag.
- `implTorqueDEM` — treat torque implicitly on the DEM side, mirroring `implForceDEM` for particle drag.
- `voidageFunctionDiFelice` / `voidageFunctionRong` / `voidageFunctionTang` — mutually-relevant voidage correction functions for the drag calculation (DiFelice, Rong, Tang); if a non-default one of these is `true`, the others must be `false`.
- `particleSpecificCG` — activate particle-specific coarse graining, i.e. every particle communicates its own coarse-graining factor.

### First-`forceSubModel`-only keywords

These are only read from the *first* `forceSubModel` listed for a given `forceModel`:

- `scale` (default `1`) — coarse-graining factor: `d_sim = scale * d_real`. Forces are computed for the real particle diameter then scaled for the parcel's particle count. **Applies globally** — affects every `forceModel` in the case, and overrides the coarse-graining value set in the Aspherix input script for all CFD-side computations.
- `scaleDrag` (default `1`) — scales the drag force computed by this force model directly.
- `scaleDragPerType` (default `1` per template) — per-particle-template list of drag scaling factors; supersedes `scaleDrag`. Requires `save_template_information` on the DEM side for spheres/superquadrics, and the list order must match the DEM-side particle template definition order exactly.
- `scaleTorque` (default `1`) — scales the torque computed by this force model.
- `scaleDH` (default `1`) — scales the particle-diameter-to-hydraulic-diameter ratio, affecting only this force model's drag correlation (unlike `particleShapeProps.DHc` in `couplingProperties`, which affects every force model using the clump diameter/voidfraction). Both can be used simultaneously since neither affects the voidfraction itself.
- `scaleDHPerType` (default `1` per template) — per-particle-template list version of `scaleDH`; supersedes it. Same DEM-side template-order requirement as `scaleDragPerType`.
