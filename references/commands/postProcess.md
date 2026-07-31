# postProcess

Apply a function object to a case's existing results without re-running the solver.
Use this to add a probe, force, or field calculation retroactively — you don't need to have anticipated it at the start of the run, and you don't need to re-solve to get it.

## `postProcess` the utility vs `<solver> -postProcess` the flag

These are two different things and it's easy to conflate them.

The standalone `postProcess` utility documented on this page only has access to fields already written to disk.
It cannot regenerate a field that the solver computed internally but never wrote out — it has no access to the solver's model objects (its thermophysical model, turbulence model, etc.), only whatever ended up in the time directories.

Most solvers — both stock OpenFOAM solvers and the CFDEM solver family (`cfdemSolver*`) the same way — additionally accept a `-postProcess` command-line flag on the solver binary itself:

```
<solverName> -postProcess -func <functionObjectName>
```

This runs the actual solver executable in a post-processing mode: it reconstructs the solver's runtime model objects (equations of state, thermophysical/transport models, turbulence models, the CFDEM coupling objects) for each requested time step, then evaluates the function object against that reconstructed state.
Because of that, `<solverName> -postProcess` can produce derived fields the standalone `postProcess` utility cannot — for example regenerating `rho` from `T` via the case's thermophysical model, when `rho` itself was never written to disk.

Reach for `<solverName> -postProcess` instead of the standalone `postProcess` utility whenever the field you need is *derived* from the solver's internal model rather than stored directly — check `references/RULES.md` for which fields the CFDEM solvers commonly need reconstructed this way.

## Running a function object already defined in the case

```
postProcess -func <functionObjectName>
```

`<functionObjectName>` refers to an entry under the `functions { … }` block in `system/controlDict`, or a dictionary of the same name under `system/`.
This re-executes that function object across the case's existing time directories rather than during a live solve.

## Running a built-in function object ad hoc

```
postProcess -func "mag(U)"
postProcess -func writeCellCentres
```

Many simple function objects can be invoked directly by name without being predefined in `controlDict` — useful for a one-off field derivation you don't want to leave wired into the case's normal run configuration.

## Restricting the time range

```
postProcess -func <name> -time '100:200'
postProcess -func <name> -latestTime
```

Use `-time` with a range when you only need results over part of the run (e.g. after the flow has settled), and `-latestTime` when you only care about the final state.
Check the available times first with `foamListTimes` (see `references/commands/foamListTimes.md`) rather than guessing the range.

## Multi-region cases

```
postProcess -func <name> -region <regionName>
```

As with `checkMesh`, pass `-region` explicitly for multi-region cases — the default invocation only processes the default region.

## Gotchas

- `postProcess` reads whatever is already written to disk; it does not re-solve the governing equations, so it can't retroactively compute anything that depends on data the solver didn't write out (e.g. a quantity that needed to be accumulated during the time loop, not derived from stored fields). Use `<solverName> -postProcess` instead in that case — see above.
- Verify the exact set of available function objects and flags for your OpenFOAM 10 build with `postProcess -help` rather than assuming a flag from a different OpenFOAM version applies. Same caveat for `<solverName> -postProcess -help` on a given CFDEM solver.
