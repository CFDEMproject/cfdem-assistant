# CFDEM Solvers

The `cfdemSolver*` binaries are the actual coupled CFD-DEM executables — each is a modified OpenFOAM solver with CFDEMcoupling's particle-coupling machinery layered on top.
Picking the right one is a physics decision (unresolved vs. resolved/immersed-boundary, incompressible vs. scalar-transport, particle shape support), made before touching `couplingProperties` — the model selections available there depend on which solver is running.
Launch the chosen solver with `cfdemSimulate -s <solverName>` (see `references/commands/cfdemSimulate.md`), never by invoking the binary directly.
Source: [`List_solvers.html`](https://doc.aspherix-dem.com/coupling/List_solvers.html) and each solver's own page — see `references/CFDEM_DOC_SEARCH.md`.

## Available solvers

| Solver | Based on | Use for |
|---|---|---|
| `cfdemSolverPiso` | `pisoFoam` | The baseline unresolved (Eulerian-Lagrangian, volume-averaged) CFD-DEM solver — single-phase incompressible, PISO. Start here unless a specific need below applies. |
| `cfdemSolverPisoScalar` | `pisoFoam` | `cfdemSolverPiso` plus a scalar transport equation (temperature `T`, with `TSource`/`alphat`/`Pr`/`Prt`) for convective heat transfer between fluid and particles. |
| `cfdemSolverPimple` | `pimpleFoam` | `cfdemSolverPiso` plus RANS/LES turbulence and the PIMPLE algorithm (`nOuterCorr > 1` in `fvSolution`'s `PIMPLE` sub-dict). Also the solver to reach for when using a `smoothingModel` (see `references/models/smoothingModels.md`) or `couplingProperties`' `expCorrDeltaUError`. |
| `cfdemSolverPisoNonspherical` | `pisoFoam` | Same governing equations as `cfdemSolverPiso`, but supports non-spherical particle shapes (multi-sphere, superquadric, convex) — use whenever `particleShapeType` isn't plain `"sphere"`. |
| `cfdemSolverIB` | OpenFOAM incompressible toolbox | The resolved, immersed-boundary solver — for particles whose diameter *exceeds* the local cell size, where the unresolved volume-averaging approach above breaks down. Requires IB-specific model selections (see below); not a drop-in replacement for `cfdemSolverPiso`. |

Every unresolved solver above (`cfdemSolverPiso`, `cfdemSolverPisoScalar`, `cfdemSolverPimple`, `cfdemSolverPisoNonspherical`) auto-creates `voidfraction`, `f`, `Ksl`, `Us`, and `rho` fields at runtime with default boundary conditions (`zeroGradient` or the patch's geometric constraint) — only add a file for one of these under `0/` if a non-default BC or initial value is actually needed (most commonly `voidfraction` at an inlet/outlet particles cross).

### `cfdemSolverIB` specifics

Algorithm per timestep: Aspherix advances particle motion using the previous step's velocity/pressure field → the Navier-Stokes equations solve on the whole domain ignoring the solid phase → each particle is located as a cluster of covered cells → the velocity/pressure field is corrected using that location and the particles' (angular) velocity.
Requires its own locate/void-fraction/force model selections in `couplingProperties`: `engineSearchIB` (locate), `IBVoidfraction` (void fraction), `ArchimedesIB`/`ShirgaonkarIB` (force) — see `references/models/locateModels.md` and `references/models/voidFractionModels.md`.

## Solvers withheld from the public docs

`List_solvers.html` also lists `cfdemSolverBubble`, `cfdemSolverChem`, `cfdemSolverForcingIB`, `cfdemSolverHFDIBMScalar`, `cfdemSolverInter` (the VoF solver referenced in `references/dictionaries/couplingProperties.md`'s VoF settings), `cfdemSolverMultiPhaseEuler`, `cfdemSolverRhoPimple`, and `cfdemRhoChtMultiRegion`.
Their pages return HTTP 200 with a placeholder body ("*The page you requested cannot be found. Most likely this is because the particular feature is not enabled by your license.*") rather than a real 404 — don't mistake that for a broken link or spend a fetch-strategy escalation retrying it (see `references/CFDEM_DOC_SEARCH.md`).
If one of these is actually needed for a case, its syntax isn't publicly documented; check the CFDEMcoupling source tree (`src/lagrangian/cfdemParticle/`) or internal DCS material instead of guessing from the solver name alone.
