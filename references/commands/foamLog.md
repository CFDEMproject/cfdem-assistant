# foamLog

Extract residual and convergence data from a solver's log file into plain-text columns.
Use this when diagnosing a stalled or diverging run from `log.<solverName>` — it turns a wall of solver stdout into per-field data files you can inspect or plot, instead of eyeballing scrolling residual lines.

## Basic usage

```
foamLog log.cfdemSolverPiso
```

Run in the directory containing the log file.
This writes extracted columns (one file per field/quantity, e.g. residual history for `p`, `Ux`, `Uy`, `Uz`, Courant number) into a `logs/` subdirectory.

## Reading the extracted data

The files under `logs/` are plain columns of iteration/time vs. value — read them directly, or plot with `foamMonitor -l logs/<file>` for a live-updating plot while a run is still in progress.

## When to reach for this instead of grepping the log

Grepping `log.<solverName>` for a single field's final residual is fine for a quick check.
Reach for `foamLog` when you need the *trend* — whether residuals are decreasing, stalled, or oscillating — since that shape is what actually distinguishes a slow-but-converging case from a genuinely diverging one.
