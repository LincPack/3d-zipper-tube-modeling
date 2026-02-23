# 3D_Zipper_Tube_Modeling

This repository provides a way to model any zipper tube, provided the user can supply angles and lengths for the tube.

## Virtual Enviroment Information

### Introduction
Creating a virtual enviroment in python is a great way to seperate different coding projects on your system. A virtual enviroment allows you to select an interpreter, download project-specific packages, and run code so that the code will work the same for anyone on any system. The virtual enviroment takes packages listed in the requirements.txt file and downloads those specific files. 

It is important to note that this step is not necessary. It just provides a great way to organize things on your computer.

### Setup
- You can either clone the repository first, or create a virtual enviroment. I would recommend creating cloning the repository first, and then you can create a virtual enviroment in the same folder by going onto VS Code in the folder with the repository, and using the ctrl+shift+p to bring up the command lines. 
- You can then search for and select create a virtual enviroment. I've been using .venv types mostly. 
- After your enviroment is created, you need to download the files listed in the requirements.txt file. Head to the terminal, locate the same folder, and type **source venv/bin/activate** for linux/mac, or **.venv\Scripts\activate.bat** for windows. This command sources your virtual enviroment, after which you can use **pip install -r requirements.txt** to download all the files you need to your computer

## Exporting panels

The `Tube` class now includes an `export_panels_dxf` method that writes the
outline of each zipper‑tube panel to a simple DXF (R12) file.  No additional
packages are required – the function emits plain ASCII DXF which can be
opened by any CAD program.

Example use::

```python
from TubeMaker import Tube

# build some geometry
tube = Tube(10,5)
tube.add_joint(20,90,90)
# ... add more segments ...

# produce separate DXF files, all geometry on layer '0'
tube.export_panels_dxf(filename_prefix="mypanels", scale=1.0)

# write everything into a single DXF and give it a custom layer
tube.export_panels_dxf(filename_prefix="combined", scale=1.0,
                        layer_name="panels", single_file=True)
```

Notes:
* ``layer_name`` controls the DXF layer; setting it to ``"0"`` ensures
  compatibility with Inkscape and most CAD tools.
* ``single_file`` makes it convenient to share one drawing containing all
  panels instead of a collection of separate files.
