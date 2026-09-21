# Building O-grid meshes with classy_blocks

[classy_blocks](https://github.com/damogranlabs/classy_blocks) generates `blockMeshDict` for round domains — prefer it over hand-derived vertex/block math. Fetch `examples/shape/cylinder.py`/`examples/optimization/*.py` from the repo directly; the pip package ships no `examples/`.

## Setup

Depends on `numba`, which can conflict with a system-installed `numba`/`numpy` pair. Run via `uv run` with inline PEP 723 dependencies to sidestep it.

## A working, uniformly-smoothed cylinder O-grid

```python
import classy_blocks as cb

cylinder = cb.Cylinder(
    [0.0, 0.0, 0.0],          # axis start
    [TUBE_LENGTH, 0.0, 0.0],  # axis end -- also sets axis direction/length
    [0.0, 0.0, TUBE_RADIUS],  # a point on the start face's radius
)

# start_size ONLY (no end_size) on all three -- uniform, near-cubic cells,
# no near-wall clustering (passing both grades toward one end instead).
cylinder.chop_axial(start_size=cell_size)
cylinder.chop_radial(start_size=cell_size)
cylinder.chop_tangential(start_size=cell_size)

cylinder.set_start_patch("inlet")
cylinder.set_end_patch("outlet")
cylinder.set_outer_patch("wall")

mesh = cb.Mesh()
mesh.add(cylinder)
mesh.modify_patch("wall", "wall")   # patch TYPE (wall/patch/...), not just a name
mesh.write("system/blockMeshDict")
```

`chop_radial` internally rescales `start_size` by the core/shell ratio so cells stay continuous in size across that interface — don't hand-correct for it.
