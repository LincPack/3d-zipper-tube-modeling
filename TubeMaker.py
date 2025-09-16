import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, tan, arctan
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Tube:

    def __init__(self, width, height, alpha):
        self.width = width
        self.height = height
        self.alpha = alpha

        self.num_sections = 0
        self.base = [[[0, 0, 0], 
                     [width, 0, 0], 
                     [width+self.height/np.tan(self.alpha), 0, height], 
                     [self.height/np.tan(self.alpha), 0, height]]]
        
        self.working_points = [p.copy() for p in self.base]
        self.sections = []
        self.sections.append(self.base)
        self.transformations = []
 
    def add_joint(self, l, theta):
        self.transformations.append(self.trans2D([l, theta]))
        self.num_sections += 1
        print(f"Joint added with the following parameters: l:{l}, theta:{theta}")
        return

    def rm_joint(self, num_joint_removed):
        counter = num_joint_removed
        while self.num_sections > 0 and counter > 0:
            self.sections.pop()
            counter -= 1
            self.num_sections -= 1
        print(f"{num_joint_removed} joint(s) removed")
        return

    def trans2D(self, l, theta):
        
        return np.array([[1, 0, 0, 0],
                         [0, -cos(2*arctan(sin(self.alpha)*tan(theta))), -sin(2*arctan(sin(self.alpha)*tan(theta))), l],
                         [0, sin(2*arctan(sin(self.alpha)*tan(theta))), -cos(2*arctan(sin(self.alpha)*tan(theta))), 0],
                         [0, 0, 0, 1]])

    def visualize(self):
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        ax.set_xlim([0, 2*self.height])
        ax.set_ylim([0, 2*self.height])
        ax.set_zlim([0, 2*self.height])

        ax.plot([0, 2], [0, 0], [0, 0], color='r')  
        ax.plot([0, 0], [0, 2], [0, 0], color='g')  
        ax.plot([0, 0], [0, 0], [0, 2], color='b')

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        # Obtaining List of points
        print("Obtaining list of points")

        # Plotting the boxes
        boxes = Poly3DCollection(self.base, alpha=0.25, facecolor='cyan', edgecolor = "black")
        ax.add_collection3d(boxes)    
        
        plt.show()