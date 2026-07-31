# couplingProperties

The central CFDEM coupling dictionary: it configures the coupling routines between the CFD and DEM sides of a coupled simulation.
Location: `$caseDir/CFD/constant/couplingProperties`.
Source: local CFDEM coupling docs, `settings_coupling.html` — see `references/CFDEM_DOC_SEARCH.md` for how to look up the full page yourself.

The dictionary is split into two parts.
**Model selection & global settings** (documented here) picks which sub-models are active and sets a handful of case-wide values.
**Sub-model properties** are separate sub-dictionaries configuring each selected model individually — those settings live on that model's own doc page (e.g. a chosen `forceModel`'s properties are documented alongside that force model), not here.

## Model selection

Each entry below selects which implementation of a model family is active.
See the corresponding `List_<family>.html` page (via `references/CFDEM_DOC_SEARCH.md`) to see every available option for a given family before picking one.

- `voidFractionModel` — which void-fraction model to use. No default; must be set.
- `locateModel` — which particle-locate model to use. No default; must be set.
- `dataExchangeModel` — which data-exchange model to use. Default: `twoWaySocket`.
- `meshMotionModel` — which mesh-motion model to use. Default: `noMeshMotion`.
- `IOModel` — which IO model to use. Default: `noIO` — with the default, CFDEMcoupling writes no extra particle data itself; DEM output is instead triggered on every CFD write time (see `writeAsx`).
- `probeModel` — which probe model to use. Default: `noProbe`.
- `averagingModel` — which averaging model to use. Default: the dense averaging model.
- `clockModel` — which clock model to use. Default: `noClock`.
- `smoothingModel` — which smoothing model to use. Default: `noSmoothing`.
- `forceModels` — list of force models to use. No default; must be set (type: list).
- `postProcessingModels` — list of post-processing models to use (type: list). Default: `checkCouplingInterval` and `checkFluxBalance`.
- `asxCommands` — list of command models to use (type: list). Default: `(runAsx writeAsx)` — loads the models that run Aspherix and write restart files. Also check the `enable_cfd_coupling` command's own docs for how Aspherix interacts with CFDEMcoupling from the DEM side.
- `momCoupleModels` — list of momentum-couple models to use (type: list). Default: set by the solver — by default, whichever models the chosen solver supports. Users can restrict this list further; a model not supported by the solver cannot be used regardless.
- `turbulenceModelType` — file name of the dictionary used to configure turbulence models. **Not available** on versions compiled against OpenFOAM 8 and higher — irrelevant for this skill's OpenFOAM 10 target; don't set it.

## Model and parameter settings

- `modelType` — which formulation of the coupled equations to solve, per Zhou et al. (2010), *"Discrete particle simulation of particle-fluid flow: model formulations and their applicability"*, JFM.
  - `"A"` — corresponds to model type II in Zhou et al.; requires the `gradPForce` and `viscForce` force models.
  - `"B"` — corresponds to model type III in Zhou et al.; requires the `Archimedes` force model.
  - `"Bfull"` — corresponds to model type I in Zhou et al.
- `fluidDensity` — the fluid density. Only used by single-phase incompressible solvers: `cfdemSolverPiso`, `cfdemSolverPisoScalar`, `cfdemSolverPimple`, `cfdemSolverIB`.
- `particleShapeType` — which particle shape is used. Default: `"sphere"`. Other valid values: `"multisphere"`, `"superquadric"`, `"convex"`.
- `particleShapeProps` — dictionary (type: dictionary) with further shape-related settings:
  - `DHc` — scale factor for clump diameter (and thus volume) per clump type, as a `scalarList` matching the number of particle shapes. Default `1` per type. The diameter is derived from the clump volume Aspherix computes (a Monte Carlo integration over the clump's spheres, or from mass and density — see the `particle_template` command); note this is a *hydraulic* diameter (an equal-volume sphere's diameter).
  - `area` — surface area per clump type. Computed automatically as an equal-volume sphere's surface area when the user-entered value is negative; mixed manual/automatic settings across clump types are allowed.
- `solveFlow` — switch (default `true`) for whether the fluid equations are solved at all. Set `false` to make the fluid solver inactive.
- `couplingInterval` — integer: number of DEM time steps between CFD-DEM data exchanges. Defaults so that data exchanges every CFD time step. **Constraint**: the CFD time step must be a multiple of `DEM time step * couplingInterval` — i.e. the CFD time step must be larger than `DEM time step * couplingInterval`. Example: `DEMts = 1e-5`, `CFDts = 1e-4` ⟹ `couplingInterval = 10` (exchange every 10 DEM steps, i.e. every `1e-4 s`).
- `expCorrDeltaUError` — switch (default `false`). For solvers handling explicit volumetric forces on the fluid: implicit force coupling leaves a small Newton's-third-law violation between the force on the particles and on the fluid (`TotalError(dU) = Ksl*(Uf_preStep - Uf_postStep)`, since particles only ever experience `Uf_postStep`). Setting this `true` corrects for that error explicitly — typically at the cost of a less stable solution. The normalized error (relative to total implicit drag) is displayed during the run.
- `useDDTvoidfraction` — how to compute the time derivative of voidfraction. Default `"off"`.
  - `"a"` — computed from divergence of mapped particle velocities: `fvc::div(Us*(1 - voidfraction))`.
  - `"b"` — direct variant: `fvc::ddt(voidfraction)`.
  - `"off"` — ignore the time derivative (`ddt(voidfraction) = 0`); default because this field otherwise varies substantially in time and space, hurting numerical stability. An exclusion mask for `ddt(voidfraction)` can be configured in the void-fraction model itself.
- `verbose` — switch (default `false`) for extra debugging output on the coupling procedure.
- `fieldVerbosity` — integer (default `0`). Nonzero (most solvers use `1`) triggers writing additional fields (e.g. `Us`) intended for debugging; `0` writes none of the extras.
- `fixedFluxPressureCheck` — switch (default `true`). Enforces that pressure boundary conditions use `fixedFluxPressure`, not `zeroGradient`. Set `false` only if you deliberately want `zeroGradient` pressure BCs.

## Extra settings for concave particles

- `concaveWeightList` — list (type: list). In Aspherix/CFDEMcoupling, concave particles are represented as an assembly of convex particles; when `particleShapeType "convex"` is used, this list gives each convex particle's volume-contribution weight toward its parent concave object.
  Example, two concave particles (three and two convex particles respectively, five convex types total):
  ```
  particleShapeType "convex";
  concaveWeightList
  (
      0.3 0.5 0.2   // contributions to first concave
      0.5 0.5       // contributions to second concave
  );
  ```
  **Order matters**: weights must be listed in the same order the convex particle types were defined in Aspherix's particle templates.

## Settings for Volume-of-Fluid (VoF) solvers

Applies to `cfdemSolverInter`.
Discontinuities at the fluid-fluid interface (e.g. in the pressure field) make interpolation and gradients calculated across that interface numerically delicate or meaningless, so VoF cases carry extra restrictions.

- `noParticlesAtInterface` — switch (default `false`). Forces the user to explicitly confirm particles are not close to the liquid-gas interface, required whenever pressure gradients are used (via the `gradPForce` force model) or any force model interpolates fluid fields to particle positions.
- `phaseChange` — switch. Default: `true` if a temperature field `T` exists in the start-time directory, `false` otherwise. Controls whether phase change / the temperature field is solved for; can be overridden manually (see `cfdemSolverInter`).

## IB settings

Relevant when using an IB-style locate model (e.g. `engineIB`), where periodic boundaries need to be declared explicitly in `couplingProperties` — especially if particles cross that periodic boundary.
Example case: `tutorials/cfdemSolverIB/periodicSettling`.

- `checkPeriodicCells` — switch (default `false`). Check for particles in cells at periodic boundaries.
- `wall_blockPeriodicityCheck` — dictionary (type: dictionary), one entry per coordinate direction; each controls whether periodicity checks run in that direction. Default `false` for each direction.
- `wall_periodicityCheckTolerance` — scalar (default `1e-7`). Tolerance for wall periodicity checks.

Example:

```
// handle periodic wall
checkPeriodicCells true;
wall_blockPeriodicityCheck
{
    x true;
    y true;
    z false;   // periodic in this direction
}
wall_periodicityCheckTolerance 1e-8;
```
