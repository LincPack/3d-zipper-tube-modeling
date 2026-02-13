#%%
from TubeMaker import Tube
import numpy as np

master = Tube(10, 5, 60, 60, 70)
master.add_joint(15, 30, 100)
master.add_joint(25, 50, 80)



master.visualize('t')

# master.create_prototype(.1, 10)