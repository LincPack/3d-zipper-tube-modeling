# 3D_Zipper_Tube_Modeling

This repository provides a way to model any zipper tube, provided the user can supply angles and lengths for the tube.

A Python package (`zipper-tube`) wraps the core `Tube` class; the API is exposed via
```python
from zipper_tube import Tube
```


## Virtual Enviroment Information

### Introduction
Creating a virtual enviroment in python is a great way to seperate different coding projects on your system. A virtual enviroment allows you to select an interpreter, download project-specific packages, and run code so that the code will work the same for anyone on any system. The virtual enviroment takes packages listed in the requirements.txt file and downloads those specific files. 

It is important to note that this step is not necessary. It just provides a great way to organize things on your computer.

### Setup
- Clone the repository and optionally create a virtual environment in the project folder (e.g. `python -m venv .venv`).
- Activate the environment (`source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\activate.bat` on Windows).
- Install the package and development dependencies:
  ```sh
  pip install -e .[dev]
  ```
  (or `pip install .` for a normal install; `requirements.txt` is kept for compatibility.)


## Usage

### Creating a Tube

```python
from zipper_tube import Tube

# Create a tube with width 10, height 5, default angles
tube = Tube(10, 5)
```

### Adding Joints

Add segments to the tube by specifying length and angles (in degrees):

```python
# Add a joint: length 20, theta 90°, gamma 90°
tube.add_joint(20, 90, 90)

# Add another joint
tube.add_joint(15, 45, 60)
```

### Visualization

Visualize the tube as reflecting planes or physical tube:

```python
# Show reflecting planes (default)
tube.visualize()

# Show physical tube
tube.visualize(rep_method='t')
```

### Animation

Display a folding animation:

```python
# Show animation and save as GIF
tube.show_animation(save=True)
```

![Demo](assets/image24.gif)

### Exporting Panels

Export panel outlines to DXF files for CAD:

```python
# Export each panel to separate files
tube.export_panels_dxf(filename_prefix="mypanels", scale=1.0)

# Export all panels to one file with custom layer
tube.export_panels_dxf(filename_prefix="combined", scale=1.0,
                        layer_name="panels", single_file=True)
```

### Inspecting Coordinates

Print corner coordinates for debugging:

```python
tube.print_points()
```

## API Reference

### Tube(width, height, alpha=90, theta=90, gamma=90)

Create a new zipper tube model.

- **width**: Length of parallelogram sides along x-axis
- **height**: Height along z-axis  
- **alpha**: Deployment angle degrees (default 90)
- **theta**: Initial rotation about x in degrees (default 90)
- **gamma**: Initial rotation about z in degrees (default 90)

### add_joint(l, theta, gamma)

Add a new segment to the tube.

- **l**: Length of the segment
- **theta**: X-axis rotation angle in degrees
- **gamma**: Z-axis rotation angle in degrees

### visualize(rep_method='p')

Display a 3D plot of the tube.

- **rep_method**: 'p' for reflecting planes, 't' for physical tube

### show_animation(save=True)

Show a rotating animation of the tube folding.

- **save**: Whether to save animation as 'tube_animation.gif'

### export_panels_dxf(filename_prefix="panel", scale=1.0, layer_name="0", single_file=False)

Export panel outlines to DXF files.

- **filename_prefix**: Base name for output files
- **scale**: Scaling factor for coordinates
- **layer_name**: DXF layer name
- **single_file**: If True, combine all panels into one file

### print_points()

Print corner coordinates of all segments to console.
