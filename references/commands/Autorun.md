# Autorun.sh / run.config test-case runner

Many CFDEM(R)coupling tutorials/unit tests are driven by a `run.config` (JSON) + `Autorun.sh` pair instead of a hand-written `run.sh`:

- `run.config` declares the run(s) (solver, `np`, `pre_scripts`, DEM input, post-processing data series/plots) as JSON.
- `Autorun.sh` is typically just:
  ```bash
  source $CFDEM_ETC_DIR/functions.sh
  runTestcaseVariant
  keepDEMrestart="false"
  keepCFDmesh="false"
  cleanCFDEMcase $casePath/CFD $keepDEMrestart $keepCFDmesh
  ```
- `runTestcaseVariant` (in `$CFDEM_ETC_DIR/functions.sh`) renders `run.config` into a concrete `run.sh` via `$CFDEM_ETC_DIR/jsonReader.py --scriptname run.sh`, executes it, then deletes the generated `run.sh`.

## `cleanCFDEMcase` deletes the results

`cleanCFDEMcase` asks for confirmation (Enter proceeds, Ctrl-C aborts) and then deletes the results of the case: the time and `processor*` directories, `postProcessing`, the logs and the DEM post-processing output.
The CFD mesh and the DEM restart files are deleted unless `keepCFDmesh` / `keepDEMrestart` is `true`.
To inspect `postProcessing/` afterwards, press Ctrl-C at the prompt.

## Known gotcha: generated `run.sh` sources pre-scripts without `./`

The script `jsonReader.py` generates for a `pre_scripts` entry looks like:

```bash
. prerun_setAlpha.sh &> log_prerun_setAlpha.sh.txt
```

`. file` / `source file` with a bare filename (no `/`) searches `$PATH` first in bash, **not** the current directory — unless `.` happens to be on `$PATH`. Since CFDEM/OpenFOAM environments populate `$PATH` with many solver/script bins but not `.`, this line fails with `file not found` even though the script sits right there in the case folder, despite `set -e` being active in the generated `run.sh`.

If you hit this and don't want to touch the generator, the pre-script can be run directly (`bash prerun_setAlpha.sh`) as a substitute for that one line — the rest of the generated `run.sh` (decompose, `cfdemSimulate`, plotting) is unaffected.
