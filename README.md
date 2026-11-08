# 3D Zipper Tube Modeling

This repository models zipper-tube geometry as a set of connected box/face segments. The main entry point is the `Tube` class in `zipper_tube/__init__.py`.

```python
from zipper_tube import Tube
```

The class supports:
- manually defining tube segments with `add_joint(...)`
- generating a tube from helical parameter values with `get_tube_from_params(...)`
- plotting the geometry with `visualize(...)`
- exporting STL/STEP/DXF meshes for fabrication or simulation
- writing MuJoCo XML geometry for physics workflows

## Installation

Clone the repository and install it into a virtual environment:

```bash
git clone https://github.com/LincPack/3D_Zipper_Tube_Modeling.git
cd 3D_Zipper_Tube_Modeling
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
# or, for an editable install:
pip install -e .

# If your environment raises "ModuleNotFoundError: No module named 'ffmpeg'",
# install the Python binding explicitly:
pip install ffmpeg-python
```

## Basic usage

### Create a tube and add joints manually

`Tube(width, height, alpha=90, theta=90, gamma=90)` uses degree-based inputs for the initial joint orientation.

```python
from zipper_tube import Tube

# Create a basic tube model
# width and height are in the same length units as the rest of the geometry
tube = Tube(width=1.0, height=1.0, alpha=90, theta=90, gamma=90)

# Add one or more segments. The values are in degrees.
tube.add_joint(l=0.5, theta=65, gamma=90)
tube.add_joint(l=0.7, theta=80, gamma=110)
tube.add_joint(l=0.6, theta=70, gamma=95)

print("sections:", tube.num_sections)
print("number of boxes:", len(tube.boxes))
```

### Visualize the tube

`visualize` uses `rep_method` to switch the plotting mode.

```python
# Show reflecting planes
tube.visualize(rep_method='p')

# Show the physical tube mesh/solid representation
tube.visualize(rep_method='t')

# Show a centerline/path-style representation
tube.visualize(rep_method='m')
```

`rep_method` values:
- `'p'`: reflecting planes
- `'t'`: physical tube
- `'m'`: path/centerline plot

### Animate the tube

```python
# Open an animation window and optionally save it as a video.
tube.show_animation(save=False, rep_method='t')
```

This creates a rolling/deployment animation using the current tube geometry.

## Generate a tube from helical parameters

The package also exposes parameterized geometry generation through `get_tube_from_params(...)`.

```python
import numpy as np
from zipper_tube import Tube

# Create a helical zipper tube from a radius and curve parameters
tube = Tube(width=1.0, height=1.0)
tube.get_tube_from_params(R=2.0, n=4, T=2 * np.pi, offset_curve=True)

# Print the computed parameter table for debugging
# tube.print_params(gammas, thetas, Ls)

# Visualize the generated geometry
tube.visualize(rep_method='t')
```

This is useful when you want to generate the tube from a smooth path instead of manually specifying each joint.

### Worked example: a planar circular curve

The default `main_curve_pt` helper describes a helix, with `z = t`. To use a
planar circle instead, edit `Tube.main_curve_pt` in
`zipper_tube/__init__.py`. The class method takes `self`, `R`, and `t`, so use:

```python
def main_curve_pt(self, R, t):
    return np.array([R * np.cos(t), R * np.sin(t), np.zeros_like(t)])
```

Then generate the tube from that curve and display its physical representation:

```python
import matplotlib.pyplot as plt
import numpy as np
from zipper_tube import Tube

tube = Tube(width=1.0, height=1.0)
tube.get_tube_from_params(R=2.0, n=4, T=2 * np.pi, offset_curve=False)
tube.visualize(rep_method="t")
plt.show()
```

`visualize(rep_method="t")` already calls `plt.show()` in the current
implementation, so the final `plt.show()` is optional. Use `offset_curve=False`
to generate the tube along the customized main curve.

## Export geometry for fabrication or simulation

### Export STL meshes

```python
# Write per-panel STL files into the stls/ directory
# The files are named panel_s<i>_f<j>.stl
tube.create_prototypes_stl(model_thickness=0.05, scale=1.0, binary=True)
```

### Export STEP files

```python
# Generate STEP panel prototypes (panel_s<i>_f<j>.step)
tube.create_prototypes(model_thickness=0.05, scale=1.0)
```

### Export DXF panel outlines

```python
# Single set of panel outlines as separate DXF files
tube.export_panels_dxf(filename_prefix="panel", scale=1.0)

# Combine all panel outlines into one DXF layer
tube.export_panels_dxf(
    filename_prefix="combined_panels",
    scale=1.0,
    layer_name="zipper_tube",
    single_file=True,
)
```

## Produce MuJoCo XML

The library can also emit a physics scene XML that references the generated STL panels.

```python
# Writes a MuJoCo XML file and loads panel meshes from ./stls
# Use Physics_Sim/Triple_tube.xml as a target path for the simulation scene
tube.produce_XML(
    filename="Physics_Sim/Triple_tube.xml",
    panel_thickness=0.01,
    mass=1.0,
    gravity=(0.0, 0.0, -9.81),
    timestep=0.002,
)
```

This is useful when creating a simulation-ready version of the zipper tube in MuJoCo.

## Debugging and inspection helpers

```python
# Print all segment corner coordinates
tube.print_points()

# Plot end-effector / path information
tube.show_path(rep_method='m')
```

## Example script

A minimal end-to-end example looks like this:

```python
import numpy as np
from zipper_tube import Tube

# Manual tube specification
tube = Tube(1.0, 1.0)
tube.add_joint(0.6, 60, 90)
tube.add_joint(0.8, 75, 100)

# Alternate: generate from helical parameters
# tube = Tube(1.0, 1.0)
# tube.get_tube_from_params(R=2.0, n=4, T=2 * np.pi, offset_curve=True)

# Show the geometry
tube.visualize(rep_method='t')

# Export mesh files
tube.create_prototypes_stl(model_thickness=0.05, binary=True)
```

## Notes

- All angle arguments are supplied in degrees, even though internal storage converts them to radians.
- `Tube` is a geometry generator; the resulting mesh/scene files are written to the current working directory unless you specify explicit output paths.
- For simulation and animation workflows, it is often easiest to generate the geometry first, then call the visualization/export methods on the finished `Tube` object.
