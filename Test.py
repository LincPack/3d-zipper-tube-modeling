from TubeMaker import Tube
import numpy as np

test = Tube(5, 5, 90)
test.add_joint(5, 100)
test.add_joint(5, 100)
test.add_joint(3, 110)
test.add_joint(5, 80)


test.visualize()
