# Rules

The single source of truth for rule *content* that applies to every CFDEM(-coupled) case built with this skill.
Other files describe *when*/*how* each rule is applied; the rule text itself must live only here — don't fork rule content into multiple places.

To be populated from internal DCS material and the public CFDEM coupling documentation (see `references/CFDEM_DOC_SEARCH.md` for how to search and fetch it), whichever applies to a given rule.

## Environment

Before running, compiling or inspecting anything with CFDEM, OpenFOAM or Aspherix tools, check that the CFDEM environment is loaded (`echo $CFDEM_PROJECT_DIR`; `cfdemSysTest` shows the full settings). If it is not, load it as described in `references/CFDEM_ENVIRONMENT.md` before doing anything else.
Use `$CFDEM_ASX_EXEC` as the Aspherix executable. `aspherix` not being on `PATH` does not mean Aspherix is not installed: it usually means the environment is not loaded. Do not conclude that something is missing or unavailable before the environment has been loaded and checked.

## Default Values

Prefer to leave a `couplingProperties`/`*Props` dictionary keyword at its documented default rather than restating it explicitly. Only set one when the case genuinely needs a value different from the default.
