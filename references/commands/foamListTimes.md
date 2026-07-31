# foamListTimes

List the time directories present in a case.
Use this before any command that takes a `-time`/`-latestTime` argument (`postProcess`, `reconstructPar`, `foamToVTK`, …) so you act on time directories that actually exist instead of guessing.

## Basic usage

```
foamListTimes
foamListTimes -case <caseDir>
```

Run from the case directory, or point at one with `-case`.
By default the initial `0/` directory is excluded — pass `-withZero` if you need it included (e.g. to confirm the initial condition was written correctly).

## Latest time only

```
foamListTimes -latestTime
```

Use this to get a single value for scripting — feeding the result into `postProcess -time <value>` or similar — rather than parsing the full list.

## Parallel cases

```
foamListTimes -processor
```

For a decomposed case, this lists the times found inside the `processorN/` directories instead of the reconstructed case root — use it to confirm a parallel run actually wrote results before running `reconstructPar`.

## Deleting time directories

```
foamListTimes -rm -time '100:200'
```

`-rm` deletes every listed time directory instead of printing it.
This is destructive and irreversible — never run it without first running the equivalent `foamListTimes -time '...'` (without `-rm`) to confirm exactly which directories match, and never run it without the user's explicit go-ahead.
