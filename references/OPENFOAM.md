# OpenFOAM Baseline

This skill targets **OpenFOAM 10** (OpenFOAM Foundation release) exclusively — this is not a preference, it's the only OpenFOAM version the current CFDEM coupling is compatible with.
Not ESI/OpenCFD releases (`openfoam.com`, e.g. v2312), and not other Foundation versions.
CFDEM-coupled cases built with this skill assume OpenFOAM 10's dictionary syntax, solver set, and directory layout; don't introduce syntax or defaults from another version without checking it applies to OpenFOAM 10 too.

OpenFOAM's own dictionaries, solvers, and boundary conditions are common enough that model training data already covers them reliably — this skill does not re-document them.
Use the links below to verify specifics (an exact dictionary key, a BC type, a solver flag) against OpenFOAM 10 specifically, instead of relying purely on recall (which may reflect a different version) or searching the open web ad hoc.

- [OpenFOAM 10 source/tutorials (GitHub)](https://github.com/OpenFOAM/OpenFOAM-10)
- [OpenFOAM.org documentation](https://openfoam.org/resources/) (Foundation)
- [OpenFOAM Wiki](https://openfoamwiki.net/)
- [CFD-Online OpenFOAM forum](https://www.cfd-online.com/Forums/openfoam/)

Anything CFDEM-specific (coupling dictionaries, particle-fluid coupling models, the `cfdemSolver*` family) is out of scope for this file — see `RULES.md` and the CFDEM coupling references instead.
