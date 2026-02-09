import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, tan, arctan
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from sympy import pprint

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

    def __init__(self, width, height, alpha=90, theta=90, gamma=90):
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
        # self.length_list.append(0)

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
        # store parameters (theta/gamma already had initial values in __init__)
        self.theta_list.append(theta_rad)
        self.gamma_list.append(gamma_rad)
        self.length_list.append(l)
        if self.num_sections == 1:
            base = np.array([self.corner_frame_f(0, 1, 1).flatten(),
                             self.corner_frame_f(0, 2, 1).flatten(),
                             self.corner_frame_f(0, 3, 1).flatten(),
                             self.corner_frame_f(0, 4, 1).flatten()])

            second_set = np.array([self.corner_frame_f(1, 1, 1).flatten(),
                                   self.corner_frame_f(1, 2, 1).flatten(),
                                   self.corner_frame_f(1, 3, 1).flatten(),
                                   self.corner_frame_f(1, 4, 1).flatten()])

            self.boxes.append(base)
            self.boxes.append(second_set)
            # keep a template of the most-recent box in case other strategies use it
            self.template = second_set.copy()

        else:
            # For subsequent joints, compute the corner coordinates of the new
            # segment (s == current self.num_sections) expressed in frame 1
            new_box = np.array([self.corner_frame_f(self.num_sections, 1, 1).flatten(),
                                self.corner_frame_f(self.num_sections, 2, 1).flatten(),
                                self.corner_frame_f(self.num_sections, 3, 1).flatten(),
                                self.corner_frame_f(self.num_sections, 4, 1).flatten()])
            self.boxes.append(new_box)

        self.num_sections += 1
        return
    
    def corner_frame_s(self, s, n):
        L_s = self.length_list[s-1]
        theta_s = self.theta_list[s]
        gamma_s = self.gamma_list[s]

        if n == 1:
            c_s_n_s = np.array([[0],
                                [L_s],
                                [0]])
            return c_s_n_s
        elif n == 2:
            c_s_n_s = np.array([[self.width],
                                [L_s - self.width * self.cot(gamma_s)],
                                [0]])
            return c_s_n_s
        elif n == 3:
            c_s_n_s = np.array([[self.width + self.height * cos(self.alpha)],
                                [L_s - self.width * self.cot(gamma_s) - self.height * self.cot(theta_s)],
                                [self.height * sin(self.alpha)]])
            return c_s_n_s
        elif n == 4:
            c_s_n_s = np.array([[self.height * cos(self.alpha)],
                                [L_s - self.height * self.cot(theta_s)],
                                [self.height * sin(self.alpha)]])
        return c_s_n_s


# This function returns the matrix needed to transform between two immediate coordinate frames. In the paper, this matrix is called T_f,f+1:


# This function returns the product of all individual matrices needed to transform the corner coordinates in frame s to frame f, resulting in one matrix that will be multiplied by c_s_n_s:
    def combined_matrix(self, s, f):
        # Make the parameter list such that parameters for segment 1 are in the second colum

        # Create list of arrays. Each array represents a matrix that transforms from one frame to the next immediate frame.
        T_list = []
        i = f
        # Note: self.length_list stores lengths for segments starting at index 0 == segment 1,
        # while theta_list/gamma_list include the initial (segment 0) values at index 0.
        # To form T_f->f+1 we use length_list[i-1] and theta_list[i], gamma_list[i].
        while i <= s - 1:
            T_i = self._trans3D(self.length_list[i-1], self.theta_list[i], self.gamma_list[i])
            T_list.append(T_i)
            i += 1

        # Matrix multiplication by mapping:
        i = 1
        T_product = T_list[0]
        while i < len(T_list):
            T_product = T_product @ T_list[i]
            i += 1
        T_combined = T_product

        return T_combined


    # This function returns the corner coordinate of segment s, corner type n, in frame f:
    # Note that this function does not currently work when (s < f), except for when (s = 0 and f = 1). This could probably be done, but it would take a lot of work, and probably wouldn't be very useful for design anyway.
    def corner_frame_f(self, s, n, f):
        if s == 0 and f == 1:
            if n == 1:
                c_s_n_f = np.array([[0],
                                    [0],
                                    [0]])
                return c_s_n_f
            elif n == 2:
                c_s_n_f = np.array([[self.width],
                                    [-self.width*self.cot(self.gamma_list[0])],
                                    [0]])
                return c_s_n_f
            elif n == 3:
                c_s_n_f = np.array([[self.width + self.height*cos(self.alpha)],
                                    [-self.width*self.cot(self.gamma_list[0]) - self.height*self.cot(self.theta_list[0])],
                                    [self.height*sin(self.alpha)]])
                return c_s_n_f
            elif n == 4:
                c_s_n_f = np.array([[self.height*cos(self.alpha)],
                                    [-self.height*self.cot(self.theta_list[0])],
                                    [self.height*sin(self.alpha)]])
                return c_s_n_f
        elif s == f:
            c_s_n_f = self.corner_frame_s(s, n)
            return c_s_n_f
        elif s > f:
            T = self.combined_matrix(s, f)
            c_s_n_s = np.append(self.corner_frame_s(s,n), np.array([[1]]), axis = 0)
            c_s_n_f = np.delete(T @ c_s_n_s, 3, axis=0)
            return c_s_n_f
        else:
            return "This code does not support situations when s < f. Please choose a frame that corresponds to your chosen segment or is less far down the tube than the segment. In other word, the condition s >= f must be true. An exception is when s = 0 and f = 1. These coordinates can be calculated if desired."

   
    
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

            # Ensure the figure is shown when visualize() is called from scripts
            plt.show()

        

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
