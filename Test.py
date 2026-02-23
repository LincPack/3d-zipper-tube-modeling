#%%
from TubeMaker import Tube
import numpy as np

master = Tube(10, 10, 90, 60, 70)
master.add_joint(30, 60, 120)
master.add_joint(30, 60, 120)
master.add_joint(20, 100, 120)
master.add_joint(10, 100, 120)
master.add_joint(5, 60, 120)



# master.visualize('t')
# master.export_panels_dxf("Spiral.dxf")
master.show_animation()
# master.create_prototypes(model_thickness=1, scale = 10)

