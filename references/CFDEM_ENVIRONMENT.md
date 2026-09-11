# CFDEM Environment

Source: [`environmentVars.html`](https://doc.aspherix-dem.com/coupling/environmentVars.html), [`Section_installation.html`](https://doc.aspherix-dem.com/coupling/Section_installation.html) (the "Make your environment persistent" section) — see `references/CFDEM_DOC_SEARCH.md` to look up the full pages yourself.

The CFDEM environment (variables, aliases, `PATH` entries) is set up by sourcing the CFDEMcoupling `bashrc`.
Check whether it's already sourced (e.g. `echo $CFDEM_PROJECT_DIR`, or run the `cfdemSysTest` alias) before assuming a fresh shell has it — commands like `cfdemSimulate` and the `cfdem*` aliases below don't exist until it is.

## Loading the environment

```
source $HOME/DCS-Computing/CFDEMcoupling-<package>-<version>/etc/bashrc
```

On `zsh`, source `etc/zshrc` from the same install directory instead.
This is a per-terminal operation — a new terminal has none of this loaded until the `bashrc`/`zshrc` is sourced again, unless made persistent (below).
After sourcing, verify it worked with the `cfdemSysTest` alias — it also reports the hyperthreading recommendation for the `twoWaySocket` data-exchange model.

If OpenFOAM or Aspherix weren't installed to their default locations, set `CFDEM_OF_DIR` and/or `CFDEM_ASX_INSTALL_DIR` (see below) *before* sourcing the `bashrc`, not after — the `bashrc` reads and then unsets them during setup.

A binary-package install may instead place this at `/opt/CFDEM/CFDEMcoupling-<package>-<version>/etc/bashrc` (or wherever it was unpacked) — adjust the path accordingly.

### Making it persistent

Options, in increasing order of flexibility:

1. Add the `source .../etc/bashrc` line directly to your `.bashrc` (or `.zshrc`) — simplest, but fixes you to one environment per shell startup.
2. Source a separate load script on demand instead of always loading it — useful once you have more than one CFDEM/OpenFOAM version and want to switch between them per-terminal rather than globally.
3. Wrap the `source` call in a shell function added to `.bashrc`, e.g.:
   ```
   loadCfdem_<version>()
   {
       # do extra environment settings like OF or Aspherix dir before sourcing the bashrc
       source $HOME/DCS-Computing/CFDEMcoupling-<package>-<version>/etc/bashrc
   }
   ```
   Call it with `loadCfdem_<version>` whenever you want that environment.
   Define one such function per version/variant you use (e.g. a GPU/SPUMA variant that also exports `CFDEM_OF_DIR` and `NVARCH` before sourcing) — this is the way to keep several installs available without them colliding.

**Only one CFDEM environment can be loaded in a shell at a time** — in particular, the GPU/SPUMA build and a normal CPU build must never be loaded simultaneously in the same shell.
If you normally auto-load one variant from `.bashrc`, disable that auto-load before switching to another variant, and re-enable it afterward.

### One-off loading without editing shell rc files

If the environment isn't sourced from `.bashrc`/`.zshrc` at all, a per-installation loader script is also available at the root of the CFDEM install: `load_CFDEMcoupling-<package>-<version>.sh`.
Source it the same way (`source .../load_CFDEMcoupling-<package>-<version>.sh`) to load the environment for just the current shell.

## Obligatory environment variables

These must resolve correctly for the environment to work; some are only needed transiently, during setup.

- `CFDEM_OF_DIR` — location of the OpenFOAM installation. Default: `$HOME/OpenFOAM/OpenFOAM-10`, falling back to `/opt/OpenFOAM/OpenFOAM-10`; the home-directory location takes precedence if both exist. **Unset automatically** by the CFDEMcoupling `bashrc` after use, specifically so it can't be accidentally reused when the environment is later reset — don't expect it to persist across a session.
- `CFDEM_ASX_INSTALL_DIR` — Aspherix installation folder (containing `bin/aspherix`). Default: auto-detected from the location of the `aspherix` executable; set manually only if that detection fails. Typical value: `$HOME/DCS-Computing/Aspherix-<version>`. Also **unset automatically** after use, same reasoning as `CFDEM_OF_DIR`.
- `CFDEM_PROJECT_DIR` — path to the CFDEMcoupling installation itself. Default: derived from the location of the sourced `bashrc`.
- `CFDEM_PROJECT_USER_DIR` — where user-created cases and solvers live. Default: `CFDEM_PROJECT_DIR` prefixed with the username (e.g. `CFDEM_PROJECT_DIR=/home/user/CFDEMcoupling-<package>-<version>` ⟹ default user dir `/home/user/user-CFDEMcoupling-<package>-<version>`). Created automatically the first time it's entered via the `cfdemRun`, `cfdemUsrSol`, or `cfdemCreateUserDir` aliases — don't assume it exists before then.

## Optional environment variables

- `CFDEM_VERBOSE` — default unset. Set to `false` to suppress the environment-settings banner normally printed when the CFDEM `bashrc` loads.
- `CFDEM_ASX_EXEC` — path to the Aspherix executable used by CFDEM scripts. Default: `$CFDEM_ASX_INSTALL_DIR/bin/aspherix`.
- `CFDEM_SOCKET_HYPERTHREADING` — `on` (default) or `off`; sets the system-wide hyperthreading default used by the `twoWaySocket` data-exchange model (see that model's own docs for the full behavior).
- `CFDEM_SIM_USE_SLURM` — does not exist by default. If set (to *any* value — only existence is checked, not the value), globally forces `cfdemSimulate` to use Slurm (`srun`) to start jobs, equivalent to passing `-useSlurm`. See `references/commands/cfdemSimulate.md`.
- `CFDEM_SIM_SLURM_SBATCH` — does not exist by default. If set (any value), globally forces `cfdemSimulate` to use resources from the executing script's own `SBATCH` pragmas, equivalent to `-useSlurmHead`.

## Further (internal) environment variables

Set internally by the CFDEM environment for convenient access to scripts/templates — not meant to be set by the user, but useful to know when tracing where something is being read from:

- `CFDEM_ETC_DIR` — the `etc` dir containing the `bashrc`, compile scripts, etc.
- `CFDEM_SCRIPT_DIR` — directory of extra scripts, automatically added to `PATH`.
- `CFDEM_DEFAULT_DIR` — directory of shared default dictionaries, meant to be `#include`d into a case's own dictionary rather than hand-copied. Notable files: `controlDefaults` (common `controlDict` entries), `probeDefaults` (common settings for a `probes` function object), `volFieldValueDefaults` (common settings for a `volFieldValue` function object). The latter two use older OpenFOAM function-object keys (`functionObjectLibs` instead of `libs`; `volFieldValueDefaults` also uses `source` instead of `regionType`) — these still work on OpenFOAM 10 (`functionObjectLibs` is a supported legacy alias, and an absent `regionType` simply defaults to the whole domain), so don't "modernize" them when including this file.
- `CFDEM_SCHEME_PATH` — directory of CFDEMcoupling's default `fvSchemes`/`fvSolution` schemes.

## Available aliases

| alias | usage | description |
|---|---|---|
| `cfdem` | `cfdem` | cd to the CFDEM install dir |
| `cfdemSrc` | `cfdemSrc`, `cfdemsrc` | cd to the CFDEM src dir |
| `cfdemEtc` | `cfdemEtc`, `cfdemetc` | cd to the CFDEM etc dir (location of `bashrc`) |
| `cfdemTut` | `cfdemTut`, `cfdemtut` | cd to the CFDEM tutorials dir |
| `cfdemSol` | `cfdemSol`, `cfdemsol` | cd to the CFDEM solvers dir |
| `cfdemUt` | `cfdemUt` | cd to the CFDEM utilities dir |
| `cfdemRun` | `cfdemRun` | cd to the CFDEM user run dir (creates `CFDEM_PROJECT_USER_DIR` on first entry) |
| `cfdemASX` | `cfdemASX` | cd to the Aspherix installation dir |
| `cfdemSysTest` | `cfdemSysTest` | sanity-check the environment settings — run this first when something seems misconfigured |
| `cfdemCompCFDEM` | `cfdemCompCFDEM` | compile CFDEMcoupling; `-h` for options |
| `cfdemAspherix` | `cfdemAspherix ./input/script/path` | run Aspherix with the given input script |
| `cfdemAspherixPar` | `cfdemAspherixPar ./input/script/path np` | run Aspherix in parallel with `np` cores |
| `cfdemUnsetEnv` | `cfdemUnsetEnv` | remove the loaded CFDEM environment (aliases, functions, variables) from the current shell |
