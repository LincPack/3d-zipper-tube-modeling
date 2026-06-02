from zipper_tube import Tube
import numpy as np

tube = Tube(0.1, 0.1, 90, 90, 90)

# tube.add_joint(1.2505, 85.99, 54.30)
# tube.add_joint(1.2505, 77.99, 154.96)
# tube.add_joint(1.2505, 101.87, 55.36)
# tube.add_joint(1.2505, 44.56, 152.20)
# tube.add_joint(1.2505, 114.63, 60.84)

# This was the original tube
tube.get_tube_from_params(R=1.5, n=12, T=np.pi*2, offset_curve= True) #n=10 for the one in the paper
# tube.visualize('t')

# tube.get_tube_from_params(R=1, n=3, T=np.pi/2) #n=10 for the one in the paper
tube.visualize('t')

# tube.show_animation()
# tube.create_prototypes(0.01, 1)

tube.show_segment_midpoint_animation(3, False, True)

# Things to try out in the code: Calculate the center of the mirror plane, then plot it as it folds up. Then I could try to make the 