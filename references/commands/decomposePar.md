# decomposePar

Split a case into subdomains for parallel (MPI) execution.
Run this before any `mpirun -np N <solver> -parallel` invocation — the solver expects `processorN/` directories to already exist, it does not decompose the case itself.

## Basic usage

```
decomposePar
```

Run from the case root, after the mesh exists (`constant/polyMesh` must already be written, e.g. via `blockMesh`) and after the initial fields are in `0/`.
Reads `system/decomposeParDict` for the number of subdomains and the decomposition method.

## Configuring the decomposition

`system/decomposeParDict` controls the split:

```
numberOfSubdomains 4;
method          scotch;
```

`numberOfSubdomains` must match the MPI rank count you'll launch with (`mpirun -np <numberOfSubdomains>`) — a mismatch is a common source of a run failing immediately on launch.
`scotch` is a reasonable default for irregular geometries; `simple`/`hierarchical` give you explicit control over the split direction (`n (nx ny nz);`) when the domain is a simple box and you want the decomposition aligned with a known flow direction.

## Re-decomposing

```
decomposePar -force
```

`-force` deletes any existing `processorN/` directories and redecomposes from scratch — use this when you've changed `numberOfSubdomains` or the mesh since the last decomposition, otherwise `decomposePar` will refuse to overwrite stale processor directories.

## Decomposing existing time results, not just the initial condition

```
decomposePar -time '0:'
```

By default only the initial time (`0/`, or whichever is `startFrom`) is decomposed.
Pass `-time` with a range to also distribute already-computed time directories across the processor subdomains — needed if you're restarting a parallel run from a case that was previously run in serial.

## Multi-region cases

```
decomposePar -allRegions
```

For a multi-region case, decompose every region in one call rather than one at a time.

## Gotchas

- Check the decomposition quality before committing to a long run: `decomposePar -cellDist` writes a `cellDist` field you can visualize to confirm the split is reasonably balanced, not lopsided across ranks.
- If the case uses a coupling or dynamic-mesh setup, confirm which regions/fields actually need decomposing — see `references/RULES.md` for anything CFDEM-coupling-specific about how the DEM side interacts with a decomposed CFD domain.
