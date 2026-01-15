import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, tan, arctan
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

"""
I'm pretty sure the only issue now is that the inital reflecting plane is not being shown correctly. All the lines travel in the correct direction,
but it isn't showing the relationship between the reflecting plane.
"""

class Tube:

    def __init__(self, width, height, alpha=90):
        """
        Create a model of a 3D zipper tube that can bend along the yz-plane.

        Parameters
        ----------

        width : float
            Line lengths of the parallogram that lie along the x-axis.
        height : float
            Height in the z-direction for the zipper tube
        alpha : float, optional (default=0)
            Angle in degrees between x-axis and the side length of the zipper tube
        
        """

        self.width = width
        self.height = height
        self.alpha = np.deg2rad(alpha)

        self.num_sections = 1
        self.base = np.array([[0, 0, 0, 1], 
                    [width, 0, 0, 1], 
                    [width+self.height/np.tan(self.alpha), 0, height, 1], 
                    [self.height/np.tan(self.alpha), 0, height, 1]])
        
        
        self.boxes = []
        self.boxes.append(self.base)
        self.transformations = []
        self.total_length = 0
        self.color_list = ['red', 'green', 'blue']
        self.theta_list = []
        self.length_list = []
 
    def add_joint(self, l, theta):
        """
        Add new section to the zipper tube.

        Parameters:
        -----------
        l : float
            Length of the defined zipper tube segment.
        theta : float
            Angle in degrees from the bottom of the zipper tube to the reflecting plane.
        """
        theta_rad = np.deg2rad(theta)
        self.theta_list.append(theta_rad)
        self.length_list.append(l)
        
        if self.num_sections == 1:

            second_set = np.array([[0, l, 0, 1],
                                   [self.width, l, 0, 1],
                                   [self.width+self.height*np.cos(self.alpha), l - self.height/np.tan(theta_rad), self.height*np.sin(self.alpha), 1],
                                   [self.height*np.cos(self.alpha), l-self.height/np.tan(theta_rad), self.height*np.sin(self.alpha), 1]])
            self.boxes.append(second_set)
        
        else:
            self.transformations.append(self._trans2D(self.length_list[-1], self.theta_list[-2]))
            total_trans = np.eye(4)
            for item in self.transformations:
                total_trans = total_trans@item

            new_box = self.boxes[1]@total_trans.T
            self.boxes.append(new_box)

        self.num_sections += 1
        print(f"Joint added with the following parameters: l:{l}, theta:{theta}")
        self.total_length = self.total_length + l*np.sin(theta_rad)
        return

    def _trans2D(self, l, theta):
        
        return np.array([[1, 0, 0, 0],
                         [0, -cos(2*arctan(sin(self.alpha)*tan(theta))), -sin(2*arctan(sin(self.alpha)*tan(theta))), l],
                         [0, sin(2*arctan(sin(self.alpha)*tan(theta))), -cos(2*arctan(sin(self.alpha)*tan(theta))), 0],
                         [0, 0, 0, 1]])

    def visualize(self, rep_method='p'):
        """
        Create a plot of the defined zipper tube.

        Parameters
        ----------
        rep_method : {'p', 't'}, optional
            Representation method to visualize the tube. Only two options are valid:
            
            - 'p' : Show reflecting planes.
            - 't' : Show the physical tube.
            
            Default is 'p'.

        Raises
        ------
        ValueError
            If `rep_method` is not 'p' or 't'.
        """
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        ax.set_xlim([-4*self.width, 4*self.width])
        ax.set_ylim([-2, 1.5*self.total_length])
        ax.set_zlim([-4*self.height, 4*self.height])


        ax.plot([0, 2], [0, 0], [0, 0], color='r')
        ax.plot([0, 0], [0, 2], [0, 0], color='g')
        ax.plot([0, 0], [0, 0], [0, 2], color='b')

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        if rep_method == 'p':
            for plane in self.boxes:
                perfect_plane = np.array([plane[0][:3], plane[1][:3], plane[2][:3], plane[3][:3]])
                ax.add_collection(Poly3DCollection([perfect_plane], alpha = 0.8, facecolor = 'cyan', edgecolor = 'black'))

        elif rep_method == 't':
            color_counter = 0
            # Plotting the boxes
            if self.num_sections > 1:
                for i in range(len(self.boxes)-1):
                    if color_counter > 2:
                        color_counter = 0
                    b1 = self.boxes[i]
                    b2 = self.boxes[i+1]

                    # build 6 faces
                    faces = [
                        [b1[0][:3], b1[1][:3], b2[1][:3], b2[0][:3]],  # side 1
                        [b1[1][:3], b1[2][:3], b2[2][:3], b2[1][:3]],  # side 2
                        [b1[2][:3], b1[3][:3], b2[3][:3], b2[2][:3]],  # side 3
                        [b1[3][:3], b2[3][:3], b2[0][:3], b1[0][:3]],  # side 4 
                        [b1[0][:3], b1[1][:3], b1[2][:3], b1[3][:3]],  # bottom
                        [b2[0][:3], b2[1][:3], b2[2][:3], b2[3][:3]]   # top
                    ]
                    ax.add_collection3d(Poly3DCollection(faces, alpha=0.8, facecolor = self.color_list[color_counter], edgecolor = "black"))
                    color_counter += 1
        
            else:
                ax.add_collection3d(Poly3DCollection(self.base, alpha=0.8, facecolor = self.color_list[color_counter], edgecolor = "black"))

        else:
            raise ValueError("rep_method must be either 'p' or 't'.")
        

        plt.show()
