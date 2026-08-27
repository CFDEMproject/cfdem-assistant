# Strategies

Short, self-contained problem-solving strategies (a few sentences each) for building and debugging CFDEM-coupled cases.
A strategy that needs its own examples or multi-step walkthrough gets its own `references/strategies/<name>.md` file, linked from here.

## Isolate the coupling interval when debugging instability

A coupled run has three independent timescales — DEM step, CFD step, coupling interval — and instability can come from any one, or their interaction. Stage the diagnosis: pure DEM, then coupled with force scaled near zero, then a small nonzero scale, then full strength — one variable at a time. `checkCouplingInterval` (`references/models/postProcessingModels.md`, made visible with `silent false`) can shortcut this.

## Size CFD cells for coarse-grained particles by local packing density, not single-particle fit

Several particles can land in one cell even when each individually fits, silently clipping a void-fraction model's solids floor (`references/models/voidFractionModels.md`). Confirm with the model's own diagnostic after sizing a mesh, not just by checking the run completes.

## Verify a suspected explanation for a quantitative gap before reporting it

A plausible story for a gap against a reference (non-sphericity, a boundary effect, mesh resolution) isn't evidence it's the actual cause — test it with an isolating before/after comparison first.
