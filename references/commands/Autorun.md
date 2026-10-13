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
