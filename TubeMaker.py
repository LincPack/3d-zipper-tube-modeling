import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Tube:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.num_sections = 1
        self.sections = [[[0, 0, 0], [width, 0, 0], [width, 0, height], [0, 0, height]]]


    def add_joint(self, parameters):
        self.sections.append([parameters])
        self.num_sections += 1
        print(f"Joint added with the following parameters: {parameters}")

    def rm_joint(self, num_joint_removed):
        counter = num_joint_removed
        while self.num_sections > 0 and counter > 0:
            self.sections.pop()
            counter -= 1
            self.num_sections -= 1
        print(f"{num_joint_removed} joint(s) removed")

    def visualize(self):
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        boxes = Poly3DCollection(self.sections, alpha=0.25, facecolor='cyan', edgecolor = "black")
        ax.add_collection3d(boxes)
        
        ax.set_xlim([0, 2*self.height])
        ax.set_ylim([0, 2*self.height])
        ax.set_zlim([0, 2*self.height])

        ax.plot([0, 2], [0, 0], [0, 0], color='r')  
        ax.plot([0, 0], [0, 2], [0, 0], color='g')  
        ax.plot([0, 0], [0, 0], [0, 2], color='b')

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        plt.show()



print("hello")