# Strategies

Short, version-independent problem-solving strategies for building and debugging CFDEM-coupled cases; coupling-specific ones are in the CFDEM notes (`scripts/ai_notes.py`, `strategies.md`).
A strategy that needs its own examples or multi-step walkthrough gets its own `references/strategies/<name>.md` file, linked from here.

## Verify a suspected explanation for a quantitative gap before reporting it

A plausible story for a gap against a reference (non-sphericity, a boundary effect, mesh resolution) isn't evidence it's the actual cause — test it with an isolating before/after comparison first.

## Validate a new or adapted case incrementally, not by running it to completion

Before trusting a freshly assembled or adapted case, run `blockMesh` → (if used) `setFields` → a short solver invocation and check it starts and steps cleanly, rather than waiting for a full physically-meaningful run.
This matters especially on a Debug build, where these solvers can be an order of magnitude slower than an optimized build, making a full run impractical to wait for.
Full quantitative validation against a reference still needs an actual complete run; "does it start up and step without error" is just the cheap, fast first check.

## Point probes need real physical time to show signal in a gravity-collapse case

In a dam-break-style setup, the interface takes on the order of `sqrt(h/g)` to move meaningfully (e.g. roughly 0.2-0.3s for OpenFOAM's classic damBreak geometry with a ~0.29m water column) — a probe placed where the front eventually arrives reads flat/near-zero noise until then.
For a quick regression check, prefer a domain-wide integrated quantity (e.g. a `volFieldValue` with `operation volIntegrate` on each phase's `alpha`) over a single point probe: it's sensitive to solver differences immediately, without needing the flow to physically travel anywhere.

## Build a coupled case in complexity stages, not all at once

Validate the simplest physics first (e.g. isothermal/momentum-only), then add the next layer (heat transfer, phase change, ...) only once that's confirmed stable — each stage is far cheaper to debug in isolation. Gate later stages behind a script variable so the same case can still run at an earlier stage for regression checking.

## Prefer classy_blocks for generating block meshes for CFD domains more complex than a single block

For a domain with geometry beyond a single-block mesh (e.g. cylindrical), prefer the `classy_blocks` Python library over deriving block/vertex/edge geometry by hand, when it's available and applicable to the case — see `references/strategies/CLASSY_BLOCKS.md`.
