from TubeMaker import Tube
import numpy as np

test = Tube(5, 5, np.pi/2)
test.add_joint(5, 80)
test.add_joint(5, 90)
test.add_joint(10, 90)

test.visualize()
