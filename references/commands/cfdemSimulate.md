# cfdemSimulate

Source: [`cfdemSimulate.html`](https://doc.aspherix-dem.com/coupling/cfdemSimulate.html) — see `references/CFDEM_DOC_SEARCH.md` to look up the full page yourself.

A shorthand bash command to launch a coupled CFDEM-Aspherix run, in serial or parallel.
Prefer this over hand-assembling `mpirun`/Aspherix/solver invocations yourself — it starts both sides with matching MPI parameters and the correct startup ordering (DEM first, opening the socket, before the CFD side connects).
Must be run from the CFD case folder (the one containing `constant`, `system`, …).

## Syntax

```
cfdemSimulate
  required arguments:
    -s -solver SOLVER     use the cfdemSolver or pure cfdSolver named SOLVER
  optional arguments:
    -i -in FILE           path to Aspherix input script FILE, setting a FILE will start Aspherix simultaneously to SOL
    -c -case FOLDER       path to the CFDEM case folder containing 0, system, constant ...
    -p -np NP             use NP number of processors in parallel
    -n -init FILE         path to Aspherix input script file to run a DEM initialization first with the same MPI parameters
    -l -location          instead of executing Aspherix in the folder the input script resides in, launch it in the CFDEM case folder
    -d -decompose         decompose CFD case before execution, runs a decomposePar -force (does not decompose by default)
    -k -keepPortOffset    keep portOffsetFiles, which are otherwise deleted by default
    -m -mpicmd CMD        change the mpi launch command to CMD, default is $mpicmd
    -o -mpiopts "OPTS"    adds custom string "OPTS" to the mpi launch command as arguments
    -b -useSlurm          use slurm as scheduler, sets mpicmd to use 'srun' and other options accordingly,
                            also set by the environment variable $CFDEM_SIM_USE_SLURM
    -r -useSlurmHead      use resources as specified by SBATCH pragmas, ignores np setting,
                            also set by the environment variable $CFDEM_SIM_SLURM_SBATCH
    -u -uniqueLogFiles    make log file names unique by appending a timestamp, i.e. keep do not override old logs,
                            this option will also change custom log file names
    -a -asxopts "OPTS"    add additional string "OPTS" to Aspherix run command, the full "OPTS" string should be quoted
    -v -var 'VAR VALUE'   set a variable in ASX script via command line
                            variable name and value must be given as space separated key value pair, enclosed in quotes
                            this option may be called several times
    -x -cfdemLog FILE     store cfdemSolver output in FILE,
                            default is $cfdemLog
    -y -asxLog FILE       store Aspherix output in FILE,
                            default is $asxLog
    -dryrun               assemble and print commands, but do not execute
    -h -help              help, display this text
```

## Examples

```
cfdemSimulate -in ../DEM/run.asx -solver cfdemSolverPiso -np 4
cfdemsimulate -solver cfdemSolverPiso -in DEM/run.asx -var "myVar 1"
cfdemSimulate -i DEM/run.asx -n DEM/init.asx -c CFD/ -s cfdemSolverPiso -np 16 -o "--oversubscribe"
cfdemSimulate -s cfdemPostproc
```

## Description

Internally starts Aspherix (with the given input script) and the chosen CFDEM solver together, both on the same number of cores.
By default, the DEM side starts first and opens the socket communication; the CFD side then connects.
Omit `-np` for a serial run (1 process each side).

`cfdemSimulate` is copied into `$CFDEM_APP_DIR` at compile time, so it behaves like any other solver in CFDEMcoupling once built.

Set `portFilePath "./";` in `twoWaySocketProps` (see `dataExchangeModel_twoWaySocket`) — reduces startup time, and required per-case to avoid socket collisions between concurrent runs.

On Slurm clusters, `-useSlurm` switches the launch command from `mpirun` to `srun` (with matching options); `-useSlurmHead` instead lets Slurm's own `SBATCH` pragmas determine resources, ignoring `-np` — coupled runs launched this way always add `--overlap`.
Both flags have environment-variable equivalents, useful for setting the behavior globally rather than per-invocation (see `references/CFDEM_ENVIRONMENT.md`):

- `CFDEM_SIM_USE_SLURM` set (to any value, `export CFDEM_SIM_USE_SLURM=""` included) ⟹ same effect as `-useSlurm`.
- `CFDEM_SIM_SLURM_SBATCH` set (any value) ⟹ same effect as `-useSlurmHead`.

Only the *existence* of these two variables matters, never their value.

When running against SPUMA as the OpenFOAM core and `-gpu`/serial mode isn't set explicitly, `cfdemSimulate` automatically adds Aspherix's `-gpu` flag and restricts execution to serial mode.

## Restrictions

Must be run from the CFD case folder (containing `constant`, `system`, etc.) — not from the DEM folder or an arbitrary working directory, even though `-i`/`-c` accept relative paths to those folders.
