from TubeMaker import Tube
import numpy as np

test = Tube(5, 5, np.pi/4)
test.add_joint(4, np.pi/8)
test.add_joint(6, -np.pi/8)

test.visualize()
