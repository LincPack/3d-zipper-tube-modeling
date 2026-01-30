import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, tan, arctan
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

"""
Redefined Tool Purpose:
- Visualize the Zipper Tubes, it would be sweet to see how it folds up
- Ensure the Zipper tube is not self-intersecting
 DF
- Show the designer the dimensions for a single zipper tube panel
- Print out the zipper tube
"""

"""Things I would like to make:
- A visualization of the 3d zipper tube transformation
- A show points method that takes in a joint and returns a matrix containing the points of the reflecting plane.
- Could I make a way to export the tube as an stl or obj file for 3d printing?
- What about printing a cutout model for the zipper tube?

"""

class Tube:

    def __init__(self, width, height, alpha=90, gamma=90, theta=90):
        """
        Create a model of a 3D zipper tube that can bend along the yz-plane.

        Parameters
        ----------

        width : float
            Line lengths of the parallogram that lie along the x-axis.
        height : float
            Height in the z-direction for the zipper tube
        alpha : float, optional (default=90)
            Angle in degrees between x-axis and the side length of the zipper tube
        gamma : float, optional (default=90)
            Angle in degrees between the 
        
        """

        self.width = width
        self.height = height
        self.alpha = np.deg2rad(alpha)
        gamma_rad = np.deg2rad(gamma)
        theta_rad = np.deg2rad(theta)

        self.num_sections = 1        
        
        self.boxes = []
        self.transformations = []
        self.total_length = 0
        self.color_list = ['red', 'green', 'blue']
        self.theta_list = []
        self.gamma_list = []
        self.length_list = []

        self.theta_list.append(theta_rad)
        self.gamma_list.append(gamma_rad)
        self.length_list.append(0)

    def csc(self, angle):
            return 1/np.sin(angle)

    def cot(self, angle):
            return 1/np.tan(angle)
 
    def add_joint(self, l, theta, gamma):
        """
        Add new section to the zipper tube.

        Parameters:
        -----------
        l : float
            Length of the defined zipper tube segment.
        theta : float
            Represents a rotation about the x-axis for the reflecting plane.
        gamma : float
            Represents a rotation about the z-axis for the reflecting plane.
        """
        theta_rad = np.deg2rad(theta)
        gamma_rad = np.deg2rad(gamma)
        self.theta_list.append(theta_rad)
        self.gamma_list.append(gamma_rad)
        self.length_list.append(l)
        
        if self.num_sections == 1:

            #This defines the base box. It uses the very first gamma and theta values which are setup when the tube is initialized.

            base = np.array([[0, 0, 0, 1], 
                    [self.width, -self.width*self.cot(self.gamma_list[0]), 0, 1], 
                    [self.width+self.height*cos(self.alpha), -self.width*self.cot(self.gamma_list[0]) - self.height*self.cot(self.theta_list[0]), self.height*sin(self.alpha), 1], 
                    [self.height*cos(self.alpha), -self.height*self.cot(self.theta_list[0]), self.height*sin(self.alpha), 1]])

            second_set = np.array([[0, l, 0, 1],
                                   [self.width, l - self.width*self.cot(gamma_rad), 0, 1],
                                   [self.width+self.height*np.cos(self.alpha), l - self.width*self.cot(gamma_rad) - self.height * self.cot(theta_rad), self.height*np.sin(self.alpha), 1],
                                   [self.height*np.cos(self.alpha), l-self.height*self.cot(theta_rad), self.height*np.sin(self.alpha), 1]])
            self.boxes.append(base)
            self.boxes.append(second_set)
        
        else:
            self.transformations.append(self._trans3D(self.length_list[-2], self.theta_list[-2], self.gamma_list[-2]))
            total_trans = np.eye(4)
            for item in self.transformations:
                total_trans = total_trans@item

            new_box = total_trans@self.boxes[1]
            self.boxes.append(new_box)

        self.num_sections += 1
        print(f"Joint added with the following parameters: l:{l}, theta:{theta}")
        self.total_length = self.total_length + l*np.sin(theta_rad)
        return        
    
    def _trans3D(self, l, theta, gamma):
        
        u_f = self.cot(theta) - cos(self.alpha) * self.cot(gamma)
        a_f = self.csc(gamma)
        b_f = np.sqrt((self.cot(gamma) - self.cot(theta) * cos(self.alpha)) ** 2 + (sin(self.alpha) * self.csc(theta)) ** 2)
        c_f = a_f * np.sqrt(u_f ** 2 + (sin(self.alpha) * self.csc(gamma)) ** 2)
        d_f = np.sqrt(((sin(self.alpha) / b_f) ** 2 + (u_f / c_f) ** 2) ** 2 + (cos(gamma) * sin(self.alpha) / b_f) ** 2 + (
                    u_f * cos(gamma) / c_f) ** 2)
        m_f = np.sqrt(cos(gamma) ** 2 + (sin(self.alpha) / b_f) ** 2 + (u_f / c_f) ** 2)
        g_f = np.sqrt((u_f / c_f) ** 2 + (sin(self.alpha) / b_f) ** 2)
        q_f = sin(self.alpha) * cos(gamma)
        r_f = sin(self.alpha) * self.cot(gamma)
        T_individual = np.array([[1/d_f*(((sin(self.alpha)/b_f)**2 + (u_f/c_f)**2)/a_f - r_f*q_f/b_f**2 + u_f**2*self.cot(gamma)*cos(gamma)/c_f**2), 1/m_f*(cos(gamma)/a_f + r_f*sin(self.alpha)/b_f**2 - u_f**2*self.cot(gamma)/c_f**2), -2*u_f*r_f/(b_f*c_f*g_f), 0],
                                [-1/d_f*(self.cot(gamma)*((sin(self.alpha)/b_f)**2 + (u_f/c_f)**2)/a_f + q_f*sin(self.alpha)/b_f**2 - u_f**2*cos(gamma)/c_f**2), 1/m_f*(sin(self.alpha)**2/b_f**2 - self.cot(gamma)*cos(gamma)/a_f - u_f**2/c_f**2), -2*u_f*sin(self.alpha)/(b_f*c_f*g_f), l],
                                [-u_f*q_f/d_f*(a_f**2/c_f**2 + 1/b_f**2), u_f*sin(self.alpha)/m_f*(1/b_f**2 + a_f**2/c_f**2), 1/(b_f*c_f*g_f)*(-u_f**2 + a_f**2*sin(self.alpha)**2), 0],
                                [0, 0, 0, 1]])
        return T_individual

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
        ax.set_ylim([-4*self.width, 4*self.width])
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
        
    def print_points(self):
        count = 0
        for item in self.boxes:
            print(f"Segment {count}:")
            print("Point 1:", item[0][:3])
            print("Point 2:", item[1][:3])
            print("Point 3:", item[2][:3])
            print("Point 4:", item[3][:3])
            print("\n")
            count += 1
        

        plt.show()
