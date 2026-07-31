# checkMesh

Run mesh quality and topology diagnostics on the mesh in `constant/polyMesh`.
Run this before handing a case off to a solver, and re-run it any time the mesh changes (after `blockMesh`, `snappyHexMesh`, or a mesh edit) — a case that fails or diverges is often a mesh problem, not a numerics problem, and `checkMesh` is the fastest way to rule that in or out.

## Basic usage

```
checkMesh > log.checkMesh 2>&1
```

Always redirect to a log file for cases of any real size — the output is long, and you'll want to grep it or diff it against a previous run.

## Deeper checks

```
checkMesh -allTopology -allGeometry > log.checkMesh 2>&1
```

`-allGeometry` adds severe non-orthogonality, cell determinant, and cell-volume-ratio checks beyond the default set.
`-allTopology` adds topological checks (cells with points used by only one face, face pyramids, etc.) that can catch mesh generation bugs the default checks miss.
Use both when investigating a solver failure — the default check alone can pass a mesh that still causes trouble.

## Moving/deforming meshes

```
checkMesh -latestTime
```

By default `checkMesh` reads the mesh in `constant/polyMesh`.
For a case with a dynamic/moving mesh, pass `-latestTime` to check the mesh as it stands at the most recent written time step instead.

## Multi-region cases

```
checkMesh -region <regionName>
```

CFDEM-coupled cases are frequently multi-region or paired with a separate DEM domain — check the specific region name if the case defines one, since the default invocation only checks the default region.

## Reading the output

The metrics that matter most, roughly in order of how often they explain a divergence:

- **Non-orthogonality**: max value above ~70 needs non-orthogonal correctors in `fvSolution`; above ~85 the mesh usually needs fixing, not just more correctors.
- **Skewness**: high skewness combined with high non-orthogonality compounds — treat the combination as worse than either alone.
- **Negative cell volumes / negative face pyramids**: must be zero; anything nonzero here means the mesh is invalid, not just poor quality.
- **The final summary line** (`Mesh OK` vs `Failed N mesh checks`) — read this first, then dig into the specific failed checks above it.

## Visualizing problem cells

```
checkMesh -writeAllFields
```

Writes cell-based fields (e.g. non-orthogonality, skewness) into the time directory so they can be visualized in ParaView — use this when a textual report isn't enough to localize where in the domain the mesh is bad.
