from TubeMaker import Tube
import numpy as np

master = Tube(5, 5, 50)
master.add_joint(5, 110)
master.add_joint(5, 110)
master.add_joint(5, 80)
master.add_joint(5, 110)
master.add_joint(5, 70)

master.visualize('t')
