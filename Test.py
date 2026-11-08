from zipper_tube import Tube
import numpy as np

tube = Tube(1.0, 1.0, 90, 90, 90)


# tube.add_joint(10, 65, 90)
# tube.add_joint(8, 80, 90)
# tube.add_joint(6, 70, 90)

tube.get_tube_from_params(2, 4, 2*np.pi, offset_curve = True)
tube.visualize('t')

# tube.combined_panels_without_hinges(0.1, 1)


# tube.visualize('t')
# tube.show_animation()
# tube.create_prototypes_stl(model_thickness = 0.01, scale = 1)

# tube.produce_XML('Physics_Sim/Triple_tube.xml')
# tube.print_points()
# tube.show_path()
