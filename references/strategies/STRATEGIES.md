# Strategies

Short, self-contained problem-solving strategies (a few sentences each) for building and debugging CFDEM-coupled cases.
A strategy that needs its own examples or multi-step walkthrough gets its own `references/strategies/<name>.md` file, linked from here.

## Isolate the coupling interval when debugging instability

A coupled run has three independent timescales — DEM step, CFD step, coupling interval — and instability can come from any one, or their interaction. Stage the diagnosis: pure DEM, then coupled with force scaled near zero, then a small nonzero scale, then full strength — one variable at a time. `checkCouplingInterval` (`references/models/postProcessingModels.md`, made visible with `silent false`) can shortcut this.

## Size CFD cells for coarse-grained particles by local packing density, not single-particle fit

Several particles can land in one cell even when each individually fits, silently clipping a void-fraction model's solids floor (`references/models/voidFractionModels.md`). Confirm with the model's own diagnostic after sizing a mesh, not just by checking the run completes.

## Verify a suspected explanation for a quantitative gap before reporting it

A plausible story for a gap against a reference (non-sphericity, a boundary effect, mesh resolution) isn't evidence it's the actual cause — test it with an isolating before/after comparison first.

## Interpolate before comparing two function-object time series

Two function objects with identical `writeControl timeStep; writeInterval 1;` can still write on different time grids — e.g. CFDEMcoupling's `probeDefaults` starts at `$deltaT` while `volFieldValueDefaults` starts at `$startTime`, and a coupled run's extra `voidfraction`/force terms can nudge `adjustTimeStep`'s Courant calculation just enough that a coupled run and its reference (uncoupled) run pick different step sizes from identical settings.
Don't assume two output files line up row-for-row; interpolate each onto a shared time array (e.g. `numpy.interp`) before comparing or plotting them.

## Validate a new or adapted case incrementally, not by running it to completion

Before trusting a freshly assembled or adapted case, run `blockMesh` → (if used) `setFields` → a short solver invocation and check it starts and steps cleanly, rather than waiting for a full physically-meaningful run.
This matters especially on a Debug build, where these solvers can be an order of magnitude slower than an optimized build, making a full run impractical to wait for.
Full quantitative validation against a reference still needs an actual complete run; "does it start up and step without error" is just the cheap, fast first check.

## Point probes need real physical time to show signal in a gravity-collapse case

In a dam-break-style setup, the interface takes on the order of `sqrt(h/g)` to move meaningfully (e.g. roughly 0.2-0.3s for OpenFOAM's classic damBreak geometry with a ~0.29m water column) — a probe placed where the front eventually arrives reads flat/near-zero noise until then.
For a quick regression check, prefer a domain-wide integrated quantity (e.g. a `volFieldValue` with `operation volIntegrate` on each phase's `alpha`) over a single point probe: it's sensitive to solver differences immediately, without needing the flow to physically travel anywhere.

## Build a coupled case in complexity stages, not all at once

Validate the simplest physics first (e.g. isothermal/momentum-only), then add the next layer (heat transfer, phase change, ...) only once that's confirmed stable — each stage is far cheaper to debug in isolation. Gate later stages behind a script variable so the same case can still run at an earlier stage for regression checking.

## Build O-grid blockMeshDicts with classy_blocks instead of hand-rolled vertex/block math

For a cylindrical CFD domain, use the `classy_blocks` Python library rather than deriving block/vertex/edge geometry by hand — see `references/strategies/CLASSY_BLOCKS.md`.

## A DEM/CFD gravity mismatch only prints a warning, not an error

DEM and CFD gravity settings (`Section_settings.html`) can silently diverge — a mismatch only shows up as a `Warning` in the log, never a fatal error.

## Use a `smoothingModel` once particles are large compared to the local cell size

See `references/models/smoothingModels.md`.

## Track the actual launch's PIDs before trusting a coupled run has ended

Per `cfdemSimulate.html`'s note on DEM/CFD process independence: check both the `aspherix` and CFD-solver PIDs from the specific launch before reusing a case's output directories.
