import matplotlib.pyplot as plt
import numpy as np
from sympy import sin, cos, tan
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from sympy import pprint
import sympy as sp
from sympy.physics.vector import dynamicsymbols
from datetime import datetime
import ffmpeg



class Tube:

    """Model and visualize a 3D zipper tube composed of connected segments.


    Instances of :class:`Tube` encapsulate the geometric parameters and

    computations required to construct a sequence of "boxes" representing the

    reflecting planes that make up a zipper-style folding tube.  The class

    supports adding joints, inspecting corner coordinates, exporting panel

    outlines (DXF/STEP), and visualizing the result via static plots or an

    animation.


    Attributes

    ----------

    width : float

        Length of the parallelogram sides aligned with the x-axis.

    height : float

        Height of each section along the z-axis.

    alpha : float

        Initial plane angle in radians (converted from degrees provided to

        ``__init__``).

    num_sections : int

        Number of segments (may start at 1 before joints are added).

    boxes : list of ndarray

        Per‑segment corner coordinates stored as 4×3 arrays.

    theta_list, gamma_list : list of float

        Lists of rotation angles (in radians) defining joint orientations.


    Notes

    -----

    * Angles ``theta`` and ``gamma`` are stored internally in radians, but

      most public APIs accept degrees for convenience.

    * Coordinate transformation methods such as ``corner_frame_f`` rely on

      linear algebra derived in the associated research paper; altering them

      should be done with care.

    """


    def __init__(self):

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

            Angle in degrees between the y-axis and the side length of the zipper tube       
        """

        theta_zero = sp.symbols('theta_0')
        gamma_zero = sp.symbols('gamma_0')

        self.t = sp.symbols('t')

        self.alpha = dynamicsymbols('alpha')

        self.alpha_dot = sp.diff(self.alpha, self.t)

        self.alpha_ddot = sp.diff(self.alpha_dot, self.t)

        self.tau = sp.symbols('tau')

        self.b = sp.symbols('b')

        self.mass = sp.symbols('m')

        self.width = sp.symbols('w')

        self.height = sp.symbols('h')

        self.num_sections = 1        

        self.boxes = []

        self.transformations = []

        self.total_length = 0

        self.color_list = ['red', 'green', 'blue']

        self.theta_list = []

        self.gamma_list = []

        self.length_list = []


        self.theta_list.append(theta_zero)

        self.gamma_list.append(gamma_zero)

        self.energies = []

        self.t_main = []

        self.t_off = []

        self.R = 0
        self.offset_curve = 0

        # self.length_list.append(0)

    # def substitute_values(self, expr=None, values=None, **kwargs):
    #     """Substitute symbolic parameters in an expression or a collection of expressions."""

    #     if values is None:
    #         values = {}

    #     if kwargs:
    #         values = {**values, **kwargs}

    #     normalized_values = {}
    #     for key, value in values.items():
    #         if isinstance(key, str):
    #             normalized_values[sp.Symbol(key)] = value
    #         else:
    #             normalized_values[key] = value

    #     if expr is None:
    #         expr = self.boxes

    #     if isinstance(expr, (list, tuple)):
    #         return [item.subs(normalized_values) for item in expr]

    #     return expr.subs(normalized_values)


    def main_curve_pt(self, R, t):
        """Return a point on the main helix curve."""
        return sp.Matrix([R * sp.cos(t), R * sp.sin(t), t])


    def offset_curve_pt(self, R, t):
        """Return a point on the corresponding offset curve."""
        return sp.Matrix([2.0 * R * sp.cos(t), 2.0 * R * sp.sin(t), t])


    def csc(self, angle):

            return 1/sp.sin(angle)


    def cot(self, angle):

            return 1/sp.tan(angle)

 
    def add_joint(self):

        """Append a new joint (segment) to the tube geometry.


        This method grows the internal representation of the zipper tube by one

        section of length ``l``.  The orientation of the reflecting plane at the

        new joint is controlled by two angles supplied in degrees: ``theta``

        (rotation about the x‑axis) and ``gamma`` (rotation about the z‑axis).


        The tube's lists of angles and lengths are updated, and a set of four

        corner coordinates for the new segment is computed and appended to

        ``self.boxes``.  On the very first call the "base" and the first

        segment are both created; subsequent calls only compute the newest box.


        Parameters

        ----------

        l : float

            Length of the added segment (same units as ``width``/``height``).

        theta : float

            Tilt angle in **degrees** about the x‑axis.

        gamma : float

            Twist angle in **degrees** about the z-axis.


        Notes

        -----

        * Angles are converted to radians for internal storage.

        * The method mutates ``self.theta_list``, ``self.gamma_list`` and

          ``self.length_list`` and increments ``self.num_sections``.

        * Returns ``None``.

        """

        theta = sp.symbols(f'theta_{self.num_sections}')
        gamma = sp.symbols(f'gamma_{self.num_sections}')
        l = sp.symbols(f'ell_{self.num_sections}')

        # store parameters (theta/gamma already had initial values in __init__)

        self.theta_list.append(theta)

        self.gamma_list.append(gamma)

        self.length_list.append(l)

        if self.num_sections == 1:

            base = sp.Matrix([self.corner_frame_f(0, 1, 1, self.alpha).flat(),

                             self.corner_frame_f(0, 2, 1, self.alpha).flat(),

                             self.corner_frame_f(0, 3, 1, self.alpha).flat(),

                             self.corner_frame_f(0, 4, 1, self.alpha).flat()])


            second_set = sp.Matrix([self.corner_frame_f(1, 1, 1, self.alpha).flat(),

                                   self.corner_frame_f(1, 2, 1, self.alpha).flat(),

                                   self.corner_frame_f(1, 3, 1, self.alpha).flat(),

                                   self.corner_frame_f(1, 4, 1, self.alpha).flat()])


            self.boxes.append(base)

            self.boxes.append(second_set)

            # keep a template of the most-recent box in case other strategies use it

            self.template = second_set.copy()


        else:

            # For subsequent joints, compute the corner coordinates of the new

            # segment (s == current self.num_sections) expressed in frame 1

            new_box = sp.Matrix([self.corner_frame_f(self.num_sections, 1, 1, self.alpha).flat(),

                                self.corner_frame_f(self.num_sections, 2, 1, self.alpha).flat(),

                                self.corner_frame_f(self.num_sections, 3, 1, self.alpha).flat(),

                                self.corner_frame_f(self.num_sections, 4, 1, self.alpha).flat()])

            self.boxes.append(new_box)


        self.num_sections += 1

        return

    
    def corner_frame_s(self, s, n, alpha):

        L_s = self.length_list[s-1]

        theta_s = self.theta_list[s]

        gamma_s = self.gamma_list[s]


        if n == 1:

            c_s_n_s = sp.Matrix([[0],

                                [L_s],

                                [0]])

            return c_s_n_s

        elif n == 2:

            c_s_n_s = sp.Matrix([[self.width],

                                [L_s - self.width * self.cot(gamma_s)],

                                [0]])

            return c_s_n_s

        elif n == 3:

            c_s_n_s = sp.Matrix([[self.width + self.height * cos(alpha)],

                                [L_s - self.width * self.cot(gamma_s) - self.height * self.cot(theta_s)],

                                [self.height * sin(alpha)]])

            return c_s_n_s

        elif n == 4:

            c_s_n_s = sp.Matrix([[self.height * cos(alpha)],

                                [L_s - self.height * self.cot(theta_s)],

                                [self.height * sin(alpha)]])

        return c_s_n_s


    def combined_matrix(self, s, f, alpha):
        # Create list of arrays. Each array represents a matrix that transforms from one frame to the next immediate frame.

        T_list = []

        i = f

        # Note: self.length_list stores lengths for segments starting at index 0 == segment 1,

        # while theta_list/gamma_list include the initial (segment 0) values at index 0.

        # To form T_f->f+1 we use length_list[i-1] and theta_list[i], gamma_list[i].

        while i <= s - 1:

            T_i = self._trans3D(self.length_list[i-1], self.theta_list[i], self.gamma_list[i], alpha)

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

    def corner_frame_f(self, s, n, f, alpha):

        if s == 0 and f == 1:

            if n == 1:

                c_s_n_f = sp.Matrix([[0],

                                    [0],

                                    [0]])

                return c_s_n_f

            elif n == 2:

                c_s_n_f = sp.Matrix([[self.width],

                                    [-self.width*self.cot(self.gamma_list[0])],

                                    [0]])

                return c_s_n_f

            elif n == 3:

                c_s_n_f = sp.Matrix([[self.width + self.height*cos(alpha)],

                                    [-self.width*self.cot(self.gamma_list[0]) - self.height*self.cot(self.theta_list[0])],

                                    [self.height*sin(alpha)]])

                return c_s_n_f

            elif n == 4:

                c_s_n_f = sp.Matrix([[self.height*cos(alpha)],

                                    [-self.height*self.cot(self.theta_list[0])],

                                    [self.height*sin(alpha)]])

                return c_s_n_f

        elif s == f:

            c_s_n_f = self.corner_frame_s(s, n, alpha)

            return c_s_n_f

        elif s > f:

            T = self.combined_matrix(s, f, alpha)

            c_s_n_s = self.corner_frame_s(s, n, alpha).col_join(sp.Matrix([[1]]))

            c_s_n_f = (T @ c_s_n_s)[:3, :]

            return c_s_n_f

        else:

            return "This code does not support situations when s < f. Please choose a frame that corresponds to your chosen segment or is less far down the tube than the segment. In other word, the condition s >= f must be true. An exception is when s = 0 and f = 1. These coordinates can be calculated if desired."

    
    def _trans3D(self, l, theta, gamma, alpha):

        
        u_f = self.cot(theta) - cos(alpha) * self.cot(gamma)

        a_f = self.csc(gamma)

        b_f = sp.sqrt((self.cot(gamma) - self.cot(theta) * cos(alpha)) ** 2 + (sin(alpha) * self.csc(theta)) ** 2)

        c_f = a_f * sp.sqrt(u_f ** 2 + (sin(alpha) * self.csc(gamma)) ** 2)

        d_f = sp.sqrt(((sin(alpha) / b_f) ** 2 + (u_f / c_f) ** 2) ** 2 + (cos(gamma) * sin(alpha) / b_f) ** 2 + (

                    u_f * cos(gamma) / c_f) ** 2)

        m_f = sp.sqrt(cos(gamma) ** 2 + (sin(alpha) / b_f) ** 2 + (u_f / c_f) ** 2)

        g_f = sp.sqrt((u_f / c_f) ** 2 + (sin(alpha) / b_f) ** 2)

        q_f = sin(alpha) * cos(gamma)

        r_f = sin(alpha) * self.cot(gamma)

        T_individual = sp.Matrix([[1/d_f*(((sin(alpha)/b_f)**2 + (u_f/c_f)**2)/a_f - r_f*q_f/b_f**2 + u_f**2*self.cot(gamma)*cos(gamma)/c_f**2), 1/m_f*(cos(gamma)/a_f + r_f*sin(alpha)/b_f**2 - u_f**2*self.cot(gamma)/c_f**2), -2*u_f*r_f/(b_f*c_f*g_f), 0],

                                [-1/d_f*(self.cot(gamma)*((sin(alpha)/b_f)**2 + (u_f/c_f)**2)/a_f + q_f*sin(alpha)/b_f**2 - u_f**2*cos(gamma)/c_f**2), 1/m_f*(sin(alpha)**2/b_f**2 - self.cot(gamma)*cos(gamma)/a_f - u_f**2/c_f**2), -2*u_f*sin(alpha)/(b_f*c_f*g_f), l],

                                [-u_f*q_f/d_f*(a_f**2/c_f**2 + 1/b_f**2), u_f*sin(alpha)/m_f*(1/b_f**2 + a_f**2/c_f**2), 1/(b_f*c_f*g_f)*(-u_f**2 + a_f**2*sin(alpha)**2), 0],

                                [0, 0, 0, 1]])

        return T_individual
    
    def _trans2COM(self, l, theta, gamma, alpha):

        """Compute the transformation matrix from the local frame of a segment to the center of mass frame."""
        
        T = self._trans3D(l, theta, gamma, alpha)
        
        # The center of mass is located at half the length of the segment along the local y-axis and half the width along the local x axis
        T_com = sp.Matrix([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, l/2],
                           [0, 0, 0, 1]])
        
        return T @ T_com

    def _build_parameter_substitutions(self, gamma_values=None, theta_values=None, length_values=None, gamma_list=None, theta_list=None, length_list=None):
        """Create a substitution dictionary for explicit numeric parameter values."""

        substitutions = {}

        def _resolve_symbols(values, symbols, name):
            if values is None:
                return
            if len(values) == len(symbols):
                source_symbols = symbols
            elif len(values) == len(symbols) - 1:
                source_symbols = symbols[1:]
            else:
                raise ValueError(f"{name} must contain {len(symbols)} entries (including the initial value) or {len(symbols) - 1} joint-only entries, received {len(values)}")
            for symbol, value in zip(source_symbols, values):
                substitutions[symbol] = value

        if gamma_values is not None:
            _resolve_symbols(gamma_values, self.gamma_list, "gamma_values")
        elif gamma_list is not None:
            _resolve_symbols(gamma_list, self.gamma_list, "gamma_list")

        if theta_values is not None:
            _resolve_symbols(theta_values, self.theta_list, "theta_values")
        elif theta_list is not None:
            _resolve_symbols(theta_list, self.theta_list, "theta_list")

        if length_values is not None:
            if len(length_values) != len(self.length_list):
                raise ValueError(f"length_values must contain {len(self.length_list)} entries, received {len(length_values)}")
            for symbol, value in zip(self.length_list, length_values):
                substitutions[symbol] = value
        elif length_list is not None:
            if len(length_list) != len(self.length_list):
                raise ValueError(f"length_list must contain {len(self.length_list)} entries, received {len(length_list)}")
            for symbol, value in zip(self.length_list, length_list):
                substitutions[symbol] = value

        return substitutions

    def get_panel_center_of_mass(self, panel_index, alpha=None):
        """Return the center-of-mass position of a given panel as a 3x1 symbolic vector."""

        if alpha is None:
            alpha = self.alpha

        if panel_index < 1 or panel_index >= self.num_sections:
            raise ValueError(f"panel_index must be between 1 and {self.num_sections - 1}.")

        corners = [
            self.corner_frame_f(panel_index, 1, 1, alpha),
            self.corner_frame_f(panel_index, 2, 1, alpha),
            self.corner_frame_f(panel_index, 3, 1, alpha),
            self.corner_frame_f(panel_index, 4, 1, alpha),
        ]

        com = sp.zeros(3, 1)
        for corner in corners:
            com += corner

        return com / 4

    def get_panel_energies(self, alpha=None, gravity=None, substitutions=None):
        """Compute potential and kinetic energy for each panel in the current tube model."""

        if alpha is None:
            alpha = self.alpha

        if gravity is None:
            gravity = sp.symbols('g')

        if substitutions is None:
            substitutions = {}

        t = sp.symbols('t')
        alpha_dot = sp.diff(alpha, t)

        self.energies = []

        for panel_index in range(1, self.num_sections):
            com_position = self.get_panel_center_of_mass(panel_index, alpha)
            com_position = com_position.subs(substitutions)

            x = com_position[0]
            y = com_position[1]
            z = com_position[2]

            potential_energy = (self.mass * gravity * z).subs(substitutions)
            x_dot = sp.diff(x, alpha) * alpha_dot
            y_dot = sp.diff(y, alpha) * alpha_dot
            z_dot = sp.diff(z, alpha) * alpha_dot
            kinetic_energy = (0.5 * self.mass * (x_dot**2 + y_dot**2 + z_dot**2)).subs(substitutions)

            self.energies.append({
                'panel': panel_index,
                'center_of_mass_position': com_position,
                'potential_energy': potential_energy,
                'kinetic_energy': kinetic_energy,
            })

        return

    def get_EOM(self, gamma_values=None, theta_values=None, length_values=None, gamma_list=None, theta_list=None, length_list=None):
        """Return the EOM after substituting explicit gamma, theta, and length values into the energies."""

        substitutions = self._build_parameter_substitutions(
            gamma_values=gamma_values,
            theta_values=theta_values,
            length_values=length_values,
            gamma_list=gamma_list,
            theta_list=theta_list,
            length_list=length_list,
        )

        self.get_panel_energies(alpha=self.alpha, substitutions=substitutions)
        print("Obtained Kinetic and Potential energies")

        P = sum(entry['potential_energy'] for entry in self.energies)
        print("Summed each panel's potential energy")
        K = sum(entry['kinetic_energy'] for entry in self.energies)
        print("Summed each panel's kinetic energy")
        # print(K)
        # K = sp.simplify(K)
        # P = sp.simplify(P)

        L = K-P

        print("Lagrangian obtained")

        LHS = sp.diff(sp.diff(L, self.alpha_dot), self.t) - sp.diff(L, self.alpha)

        # print("EOM obtained")

        RHS = self.tau - self.b*self.alpha_dot

        EOM = sp.Eq(LHS, RHS)

        # EOM_simp = sp.simplify(EOM)

        print("EOM obtained")


        return EOM



        
        

    