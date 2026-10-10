# reconstructPar

Merge a decomposed parallel run's `processorN/` results back into the single-domain case directory.
Run this after a parallel solve finishes (or partway through, to inspect intermediate results) — post-processing tools like `paraFoam` and `postProcess` expect reconstructed time directories, not per-processor ones, unless told otherwise.

## Basic usage

```
reconstructPar
```

Run from the case root.
Reconstructs every time directory found across `processorN/` into the case root, skipping any time that's already reconstructed there.

## Reconstructing only what you need

```
reconstructPar -latestTime
reconstructPar -time '100:200'
```

Use `-latestTime` when you only want to check the current state of a still-running or just-finished solve, and `-time` with a range to reconstruct a specific window — reconstructing every time step of a long run is often unnecessary and slow.
Check what's actually available first with `foamListTimes -processor` (see `references/commands/foamListTimes.md`) rather than guessing the range.

## Multi-region cases

```
reconstructPar -allRegions
```

Reconstructs every region in one call, the same pattern as `decomposePar -allRegions`.

## Excluding fields

```
reconstructPar -fields '(U p)'
```

Reconstruct only the listed fields — useful when a case has many stored fields but you only need a couple for a quick check, to avoid the time cost of reconstructing everything.

## Gotchas

- `numberOfSubdomains` must match the existing `processorN/` count, see `decomposePar.md`, "Changing the number of ranks".
- `reconstructPar` does not delete the `processorN/` directories — don't assume they're gone after reconstruction; clean them up explicitly if you need the disk space back, and only after confirming the reconstructed result is complete.
- If a parallel run crashed mid-write, the last time directory across processors may be inconsistent (some ranks wrote it, others didn't) — reconstructing that time can produce a corrupt or partial result; prefer reconstructing only up to the last time you've confirmed all processors wrote successfully.
