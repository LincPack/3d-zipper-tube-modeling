from zipper_tube import Tube
import numpy as np

tube = Tube(1, 1, 90, 90, 90)


tube.add_joint(5, 30, 45)
tube.add_joint(6, 20, 45)
tube.add_joint(3, 90, 90)

tube.create_prototypes_stl(model_thickness = 0.01, scale = 1)

tube.produce_XML('Physics_Sim/Triple_tube.xml')
# tube.print_points()
# tube.show_path()
