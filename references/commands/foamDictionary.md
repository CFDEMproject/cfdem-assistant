# foamDictionary

Query and edit OpenFOAM dictionary and field files from the CLI, without opening an editor.
Prefer this over `Read`/`Edit` on a dictionary when you only need to check or change a single entry — it parses the dictionary properly instead of relying on text matching, so it handles `#include`, macros, and regex-keyed sub-dicts (e.g. `"(k|epsilon|omega)"`) correctly.

## Reading a value

```
foamDictionary system/controlDict -entry endTime -value
foamDictionary 0/U -entry boundaryField.inlet.type -value
```

`-entry` selects an entry by dotted path through nested sub-dicts.
`-value` prints only the value, not the `key value;` pair — use this when the result feeds into a script or a decision, not when showing the user the full entry.

## Listing structure

```
foamDictionary system/fvSolution -keywords
foamDictionary system/fvSolution -entry solvers -keywords
```

`-keywords` lists the entries at the selected level without printing their values — use this to see what's defined before drilling into a specific one.

## Editing a value

```
foamDictionary system/controlDict -entry writeInterval -set 50
foamDictionary 0/U -entry "boundaryField.inlet.value" -set "uniform (2 0 0)"
```

`-set` overwrites an existing entry in place; `-add` creates a new one if it doesn't exist yet.
There is no dry-run or undo — the file is rewritten immediately.
Read the current value first (or check `git diff`/a backup) before setting, especially on a case you didn't create yourself.

## Expanding includes

```
foamDictionary system/fvSchemes -expand
```

`-expand` resolves `#include`, `#includeEtc`, and macro substitutions (`$variable`, `#calc`) and prints the fully resolved dictionary.
Use this when a dictionary references another file (common in `system/fvSchemes`/`fvSolution` when they share settings) and you need to see the effective values, not the literal text on disk.

## Gotchas

- Run it from the case directory, or pass the dictionary's full/relative path — there's no implicit case-root discovery.
- Regex-keyed sub-dicts (e.g. `"(p|U)"` in `fvSolution`) must be quoted exactly as they appear in the file when addressed via `-entry`.
- It operates on field files (`0/U`, `0/p`, …) the same way it does on `system`/`constant` dictionaries — the `boundaryField` sub-dict is just another nested entry.
