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
        self.base = np.array([[0, 0, 0, 1], 
                     [width, 0, 0, 1], 
                     [width+self.height/np.tan(self.alpha), 0, height, 1], 
                     [self.height/np.tan(self.alpha), 0, height, 1]])
        self.boxes = []
        self.boxes.append(self.base)
        self.transformations = []
 
    def add_joint(self, l, theta):
        self.transformations.append(self.trans2D(l, theta))
        self.num_sections += 1
        print(f"Joint added with the following parameters: l:{l}, theta:{theta}")
        return

    def rm_joint(self, num_joint_removed):
        counter = num_joint_removed
        while self.num_sections > 0 and counter > 0:
            self.boxes.pop()
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

        self.working_points = self.base.copy()

        for item in self.transformations:
            new_points = np.array([item @ p for p in self.working_points])
            self.boxes.append(new_points)
            self.working_points = new_points




        # Plotting the boxes
        if self.num_sections > 1:
            for i in range(len(self.boxes)-1):
                b1 = self.boxes[i]
                b2 = self.boxes[i+1]

                # build 6 faces
                faces = [
                    [b1[0][:3], b1[1][:3], b2[1][:3], b2[0][:3]],  # side 1
                    [b1[1][:3], b1[2][:3], b2[2][:3], b2[1][:3]],  # side 2
                    [b1[2][:3], b1[3][:3], b2[3][:3], b2[2][:3]],  # side 3
                    [b1[3][:3], b1[0][:3], b2[0][:3], b2[3][:3]],  # side 4
                    [b1[0][:3], b1[1][:3], b1[2][:3], b1[3][:3]],  # bottom
                    [b2[0][:3], b2[1][:3], b2[2][:3], b2[3][:3]]   # top
                ]
                ax.add_collection3d(Poly3DCollection(faces, alpha=0.3, facecolor="cyan"))

        else:
            ax.add_collection3d(Poly3DCollection(self.boxes, alpha=0.3, facecolor="cyan"))
  
        
        plt.show()
