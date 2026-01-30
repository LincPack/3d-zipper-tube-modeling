#%%
from TubeMaker3d import Tube
import numpy as np

master = Tube(10, 5, 60, 70, 60)
master.add_joint(15, 30, 120)
master.add_joint(25, 50, 60)
master.add_joint(20, 110, 45)

master.print_points()

# %%
