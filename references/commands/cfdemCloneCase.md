# cfdemCloneCase

Not covered by the public CFDEM(R)/CFDEMcoupling docs — this reference is derived from reading the script itself (`$CFDEM_PROJECT_DIR/scripts/cfdemCloneCase`, a DCS-local convenience script, shipped as a plain bash file).

Creates a clean copy of a case directory *without simulation results* — the standard way to start a new case from an existing one rather than copying the whole tree by hand.

## Syntax

```
cfdemCloneCase [OPTION] <sourceCase> <targetCase>
  options:
    -a -add <file1...N>  copy 1 or more additional files/directories from source case
                           may be given multiple times, e.g. -add settings -add CAD
    -h -help             print the usage
```

`<targetCase>` must not already exist — the script refuses to overwrite.

## What gets copied automatically

- Case root: `README`, `run.config`, any `*.sh`, `*.py`, `*.pvsm`, and the `caseSettings` directory — only if present.
- `CFD/{0,constant,system}`, plus `CFD/*.sh`, `CFD/octave`, `CFD/python` if present.
- `DEM/*.asx` (all Aspherix input scripts, e.g. `run.asx`, `materials.asx`, `particles.asx`), plus `DEM/data`, `DEM/meshes`, `DEM/restart` if present.

Anything else at the case root — results (`*.csv`, `postProcessing`, `log_*`), symlinks like `CAD`, or extensionless config files like a `settings` file read via `include_foam_variables ../settings` — is **not** copied and must be pulled in with `-add`, or recreated manually.

## Examples

```
cfdemCloneCase caseA caseB
cfdemCloneCase -add settings -add CAD caseA caseA_variant
```

## Gotchas

- **`settings` file not copied by default.** Many cases in this project drive `run.asx`/`blockMeshDict` generation from a root-level `settings` file (no extension, pulled in via `include_foam_variables ../settings`). Since it matches none of the default copy patterns, always pass `-add settings` when the source case has one.
- **`CAD` symlink not copied by default.** Cases commonly keep a `CAD -> ../CAD_central` symlink at the case root; it isn't part of any copied folder. Pass `-add CAD` to recreate it — `cp -r` (which the script uses internally) preserves a symlink argument as a symlink rather than dereferencing it, so this reproduces the link rather than inlining a copy of its target.
- **`-add` is repeatable**, so multiple extra items can be picked up in one invocation (`-add settings -add CAD`) instead of one `-add` call per file — the option only accepts a single trailing run of non-flag arguments before the mandatory `<sourceCase> <targetCase>`, so repeating `-add` is how to mix unrelated extra paths.
- `DEM/restart` *is* copied by default despite the "without results" framing — it's treated as an input (a restart/continuation point), not output. Delete it from the target afterward if a truly from-scratch case is wanted.
