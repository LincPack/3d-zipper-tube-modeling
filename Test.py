from zipper_tube import Tube
import numpy as np

tube = Tube(0.2, 0.2, 90, 90, 90)

# tube.add_joint(1.2505, 85.99, 54.30)
# tube.add_joint(1.2505, 77.99, 154.96)
# tube.add_joint(1.2505, 101.87, 55.36)
# tube.add_joint(1.2505, 44.56, 152.20)
# tube.add_joint(1.2505, 114.63, 60.84)

# This was the original tube
# tube.get_tube_from_params(R=1.5, n=10, T=np.pi*4, alpha_deg=90, w=.2, h=.2) #n=10 for the one in the paper
# tube.visualize('t')

tube.get_tube_from_params(R=2, n=4, T=np.pi*2, alpha_deg=90) #n=10 for the one in the paper
# tube.visualize('t')

# tube.show_animation()
# tube.create_prototypes(0.01, 1)
# tube.print_points()


#  54.30 85.99 1.2505
# 2 154.96 77.99 1.2505
# 3 55.36 101.87 1.2505
# 4 152.20 44.56 1.2505
# 5 60.84 114.63 1.2505

a = np.array([1.41421356, -1.41421356,  4.49778714]) # Target Curve
b = np.array([1.52341653, -1.36471617,  4.52588698]) # Actual Tube

diff = a-b
print(diff)