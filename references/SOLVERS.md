# CFDEM Solvers

The `cfdemSolver*` binaries are the actual coupled CFD-DEM executables — each is a modified OpenFOAM solver with CFDEMcoupling's particle-coupling machinery layered on top.
Picking the right one is a physics decision (unresolved vs. resolved/immersed-boundary, incompressible vs. scalar-transport, particle shape support), made before touching `couplingProperties` — the model selections available there depend on which solver is running.
Launch the chosen solver with `cfdemSimulate -s <solverName>` (see `references/commands/cfdemSimulate.md`), never by invoking the binary directly.
Source: [`List_solvers.html`](https://doc.aspherix-dem.com/coupling/List_solvers.html) and each solver's own page — see `references/CFDEM_DOC_SEARCH.md`.

## Available solvers

| Solver | Based on | Use for |
|---|---|---|
| `cfdemSolverPiso` | `pisoFoam` | The baseline unresolved (Eulerian-Lagrangian, volume-averaged) CFD-DEM solver — single-phase incompressible, PISO. Fallback for installs where `cfdemSolverPimple` isn't built (see preference note below). |
| `cfdemSolverPisoScalar` | `pisoFoam` | `cfdemSolverPiso` plus a scalar transport equation (temperature `T`, with `TSource`/`alphat`/`Pr`/`Prt`) for convective heat transfer between fluid and particles. |
| `cfdemSolverPimple` | `pimpleFoam` | `cfdemSolverPiso` plus RANS/LES turbulence and the PIMPLE algorithm (`nOuterCorrectors > 1` in `fvSolution`'s `PIMPLE` sub-dict). Also the solver to reach for when using a `smoothingModel` (see `references/models/smoothingModels.md`) or `couplingProperties`' `expCorrDeltaUError`. **Prefer this over `cfdemSolverPiso` by default**, even for laminar/single-outer-corrector cases — set `nOuterCorrectors 1` in `fvSolution`'s `PIMPLE` sub-dict and it behaves equivalently to Piso with no performance penalty, while generally being more accurate for coupled CFD-DEM and giving access to more features (turbulence, smoothing models, `expCorrDeltaUError`) if the case grows into needing them. Only reach for `cfdemSolverPiso` itself when `cfdemSolverPimple` isn't available in the install (check `ls $CFDEM_APP_DIR | grep cfdemSolver` or `which cfdemSolverPimple` — not every build compiles every solver). |
| `cfdemSolverPisoNonspherical` | `pisoFoam` | Same governing equations as `cfdemSolverPiso`, but supports non-spherical particle shapes (multi-sphere, superquadric, convex) — use whenever `particleShapeType` isn't plain `"sphere"`. |
| `cfdemSolverIB` | OpenFOAM incompressible toolbox | The resolved, immersed-boundary solver — for particles whose diameter *exceeds* the local cell size, where the unresolved volume-averaging approach above breaks down. Requires IB-specific model selections (see below); not a drop-in replacement for `cfdemSolverPiso`. |
| `cfdemSolverInter` | `interFoam` | VoF (two-phase, e.g. gas-liquid) coupled CFD-DEM, with optional mass/energy transfer between phases for melting or evaporation. Licence-gated on the public docs — see below. |
| `cfdemSolverRhoPimple` | `rhoPimpleFoam` | Compressible-flow coupled CFD-DEM (HVAC-type flows), with parcels as spheres/multi-sphere/superquadrics. Licence-gated on the public docs — see below. |
| `cfdemSolverMultiPhaseEuler` | `multiphaseEulerFoam` | Euler-Euler multi-fluid coupled CFD-DEM: an arbitrary number of fluid phases (e.g. gas bubbles dispersed in a liquid), with DEM particles coupled on top via a `voidfraction` field. Licence-gated on the public docs — see below. |

Every unresolved solver above (`cfdemSolverPiso`, `cfdemSolverPisoScalar`, `cfdemSolverPimple`, `cfdemSolverPisoNonspherical`) auto-creates `voidfraction`, `f`, `Ksl`, `Us`, and `rho` fields at runtime with default boundary conditions (`zeroGradient` or the patch's geometric constraint) — only add a file for one of these under `0/` if a non-default BC or initial value is actually needed (most commonly `voidfraction` at an inlet/outlet particles cross).

### `cfdemSolverIB` specifics

Algorithm per timestep: Aspherix advances particle motion using the previous step's velocity/pressure field → the Navier-Stokes equations solve on the whole domain ignoring the solid phase → each particle is located as a cluster of covered cells → the velocity/pressure field is corrected using that location and the particles' (angular) velocity.
Requires its own locate/void-fraction/force model selections in `couplingProperties`: `engineSearchIB` (locate), `IBVoidfraction` (void fraction), `ArchimedesIB`/`ShirgaonkarIB` (force) — see `references/models/locateModels.md` and `references/models/voidFractionModels.md`.

### `cfdemSolverInter` specifics

Based on `interFoam`'s VoF (two-phase) formulation; the liquid phase is assumed to be the first phase in the phase list.

- **Energy transport and phase change**: solved automatically if a `T` field exists at the start time (override with `couplingProperties`' `phaseChange` switch). Requires `Cp` and `k` set per phase in that phase's `physicalProperties.<phaseName>` dictionary. Phase change itself is driven by a `forceModel` (`melting`, `evaporateThermal`) plus the DEM-side `enable_particle_melting` command.
- An optional PID controller (`setPoint`, `Kp`/`Ki`/`Kd` in `phaseProperties`) can hold the fluid's center of mass in place — useful for simulating droplet evaporation without gravity to keep the fluid inside the domain.
- **Resolved (IBM) mode**: entered by selecting a particle- or arbitrary-mesh-motion `meshMotionModel` in `couplingProperties` (usage otherwise mirrors `cfdemSolverPimple`). Unlike `cfdemSolverIB`, the immersed-boundary correction here also transports the VoF indicator field `alpha`, excluding it from cells fully covered by a particle. Needs the same IB-style model selections as `cfdemSolverIB` (`engineSearchIB`, `IBVoidfraction`, `ArchimedesIB`/`ShirgaonkarIB`), plus a `solidDensity` entry in `couplingProperties` for the solid phase's density.
- Uses the same coupling fields as `cfdemSolverPimple`, with the same default-BC behavior.

### `cfdemSolverRhoPimple` specifics

Accounts for density internally (via `thermophysicalProperties`' transport/thermo/species model selection) rather than through a separate force model — **don't add an `Archimedes` force model with this solver**; it double-counts the density difference and can badly overestimate density effects, especially at high fluid/particle density ratios.
The `thermo` model's `Cp` is not used (the energy equation is switched off for this solver) even though it must still be configured.

### `cfdemSolverMultiPhaseEuler` specifics

Based on OpenFOAM's `multiphaseEulerFoam`: phases and their pairwise interaction models (drag, lift, virtual mass, heat transfer, surface tension, blending, …) are configured the normal OpenFOAM `phaseProperties` way, same as a plain `multiphaseEulerFoam` case — CFDEMcoupling only adds the particle-coupling layer on top.
Supports an arbitrary number of fluid phases, inherited from OpenFOAM's generic `phaseSystem`/`phaseModelList` — not just two, even though every shipped tutorial for this solver only demonstrates two fluid phases.

- `primaryPhaseName` (in `couplingProperties`) picks which phase's `U`/`T`/turbulence fields are used for DEM coupling. Default `"liquid"`; must be set explicitly whenever no phase in `phaseProperties` is actually named `liquid` (e.g. a `water`/`oil`/`mercury`/`air` phase set) — see `references/dictionaries/couplingProperties.md`.
- The solver adds `div(alphaRhoPhi*interpolate(voidfraction), <field>)` terms to the momentum and energy equations that don't exist in stock `multiphaseEulerFoam`. When adapting an `fvSchemes` from a plain `multiphaseEulerFoam` tutorial for this solver, add matching `divSchemes` entries for `U`, `p`/`thermo:rho`, and `K`/`e`, e.g.:
  ```
  "div\(\(alphaRhoPhi.*\*interpolate\(voidfraction\)\),U.*\)"     Gauss limitedLinearV 1;
  "div\(\(alphaRhoPhi.*\*interpolate\(voidfraction\)\),(p|thermo:rho.*)\)"  Gauss limitedLinear 1;
  "div\(\(alphaRhoPhi.*\*interpolate\(voidfraction\)\),(K|e).*\)" Gauss limitedLinear 1;
  ```

## Solvers withheld from the public docs

`List_solvers.html` also lists `cfdemSolverBubble`, `cfdemSolverChem`, `cfdemSolverForcingIB`, `cfdemSolverHFDIBMScalar`, and `cfdemRhoChtMultiRegion`.
Their pages return HTTP 200 with a placeholder body ("*The page you requested cannot be found. Most likely this is because the particular feature is not enabled by your license.*") rather than a real 404 — don't mistake that for a broken link or spend a fetch-strategy escalation retrying it (see `references/CFDEM_DOC_SEARCH.md`).
If one of these is actually needed for a case, its syntax isn't publicly documented; check the CFDEMcoupling source tree (`src/lagrangian/cfdemParticle/`) or internal DCS material instead of guessing from the solver name alone.

`cfdemSolverInter`, `cfdemSolverRhoPimple`, and `cfdemSolverMultiPhaseEuler` above are also licence-gated on the public site (their own pages return the same placeholder body as the withheld solvers) — all three are documented here instead from an internal Aspherix installation's bundled documentation (`documentation/coupling/<solver>.html`, for `cfdemSolverMultiPhaseEuler` specifically `documentation/coupling/src/cfdemSolverMultiPhaseEuler.rst`) plus, for `cfdemSolverMultiPhaseEuler`'s `fvSchemes`/phase-count notes, direct inspection of that solver's own source (`applications/solvers/cfdemSolverMultiPhaseEuler/`); re-verify against those same internal sources (not the public site) if this content needs updating later.
