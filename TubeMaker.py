import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, tan, arctan
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from sympy import pprint
from datetime import datetime


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
            base = np.array([self.corner_frame_f(0, 1, 1, self.alpha).flatten(),
                             self.corner_frame_f(0, 2, 1, self.alpha).flatten(),
                             self.corner_frame_f(0, 3, 1, self.alpha).flatten(),
                             self.corner_frame_f(0, 4, 1, self.alpha).flatten()])

            second_set = np.array([self.corner_frame_f(1, 1, 1, self.alpha).flatten(),
                                   self.corner_frame_f(1, 2, 1, self.alpha).flatten(),
                                   self.corner_frame_f(1, 3, 1, self.alpha).flatten(),
                                   self.corner_frame_f(1, 4, 1, self.alpha).flatten()])

            self.boxes.append(base)
            self.boxes.append(second_set)
            # keep a template of the most-recent box in case other strategies use it
            self.template = second_set.copy()

        else:
            # For subsequent joints, compute the corner coordinates of the new
            # segment (s == current self.num_sections) expressed in frame 1
            new_box = np.array([self.corner_frame_f(self.num_sections, 1, 1, self.alpha).flatten(),
                                self.corner_frame_f(self.num_sections, 2, 1, self.alpha).flatten(),
                                self.corner_frame_f(self.num_sections, 3, 1, self.alpha).flatten(),
                                self.corner_frame_f(self.num_sections, 4, 1, self.alpha).flatten()])
            self.boxes.append(new_box)

        self.num_sections += 1
        return
    
    def corner_frame_s(self, s, n, alpha):
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
            c_s_n_s = np.array([[self.width + self.height * cos(alpha)],
                                [L_s - self.width * self.cot(gamma_s) - self.height * self.cot(theta_s)],
                                [self.height * sin(alpha)]])
            return c_s_n_s
        elif n == 4:
            c_s_n_s = np.array([[self.height * cos(alpha)],
                                [L_s - self.height * self.cot(theta_s)],
                                [self.height * sin(alpha)]])
        return c_s_n_s


# This function returns the matrix needed to transform between two immediate coordinate frames. In the paper, this matrix is called T_f,f+1:


# This function returns the product of all individual matrices needed to transform the corner coordinates in frame s to frame f, resulting in one matrix that will be multiplied by c_s_n_s:
    def combined_matrix(self, s, f, alpha):
        # Make the parameter list such that parameters for segment 1 are in the second colum

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
                c_s_n_f = np.array([[self.width + self.height*cos(alpha)],
                                    [-self.width*self.cot(self.gamma_list[0]) - self.height*self.cot(self.theta_list[0])],
                                    [self.height*sin(alpha)]])
                return c_s_n_f
            elif n == 4:
                c_s_n_f = np.array([[self.height*cos(alpha)],
                                    [-self.height*self.cot(self.theta_list[0])],
                                    [self.height*sin(alpha)]])
                return c_s_n_f
        elif s == f:
            c_s_n_f = self.corner_frame_s(s, n, alpha)
            return c_s_n_f
        elif s > f:
            T = self.combined_matrix(s, f, alpha)
            c_s_n_s = np.append(self.corner_frame_s(s,n, alpha), np.array([[1]]), axis = 0)
            c_s_n_f = np.delete(T @ c_s_n_s, 3, axis=0)
            return c_s_n_f
        else:
            return "This code does not support situations when s < f. Please choose a frame that corresponds to your chosen segment or is less far down the tube than the segment. In other word, the condition s >= f must be true. An exception is when s = 0 and f = 1. These coordinates can be calculated if desired."

   
    
    def _trans3D(self, l, theta, gamma, alpha):
        
        u_f = self.cot(theta) - cos(alpha) * self.cot(gamma)
        a_f = self.csc(gamma)
        b_f = np.sqrt((self.cot(gamma) - self.cot(theta) * cos(alpha)) ** 2 + (sin(alpha) * self.csc(theta)) ** 2)
        c_f = a_f * np.sqrt(u_f ** 2 + (sin(alpha) * self.csc(gamma)) ** 2)
        d_f = np.sqrt(((sin(alpha) / b_f) ** 2 + (u_f / c_f) ** 2) ** 2 + (cos(gamma) * sin(alpha) / b_f) ** 2 + (
                    u_f * cos(gamma) / c_f) ** 2)
        m_f = np.sqrt(cos(gamma) ** 2 + (sin(alpha) / b_f) ** 2 + (u_f / c_f) ** 2)
        g_f = np.sqrt((u_f / c_f) ** 2 + (sin(alpha) / b_f) ** 2)
        q_f = sin(alpha) * cos(gamma)
        r_f = sin(alpha) * self.cot(gamma)
        T_individual = np.array([[1/d_f*(((sin(alpha)/b_f)**2 + (u_f/c_f)**2)/a_f - r_f*q_f/b_f**2 + u_f**2*self.cot(gamma)*cos(gamma)/c_f**2), 1/m_f*(cos(gamma)/a_f + r_f*sin(alpha)/b_f**2 - u_f**2*self.cot(gamma)/c_f**2), -2*u_f*r_f/(b_f*c_f*g_f), 0],
                                [-1/d_f*(self.cot(gamma)*((sin(alpha)/b_f)**2 + (u_f/c_f)**2)/a_f + q_f*sin(alpha)/b_f**2 - u_f**2*cos(gamma)/c_f**2), 1/m_f*(sin(alpha)**2/b_f**2 - self.cot(gamma)*cos(gamma)/a_f - u_f**2/c_f**2), -2*u_f*sin(alpha)/(b_f*c_f*g_f), l],
                                [-u_f*q_f/d_f*(a_f**2/c_f**2 + 1/b_f**2), u_f*sin(alpha)/m_f*(1/b_f**2 + a_f**2/c_f**2), 1/(b_f*c_f*g_f)*(-u_f**2 + a_f**2*sin(alpha)**2), 0],
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
        

    def create_prototypes(self, model_thickness, scale):
        """
        A function that outputs stl's of each of the panels for the individual segments. 
        
        :param model_thickness: Allows the user to specify the thickness of the resulting panel.
        """
        # For each quadrilateral face between consecutive boxes, create a thin solid by
        # extruding the quad along its normal by `model_thickness` and write a STEP file.
        if self.num_sections > 1:
            for i in range(len(self.boxes)-1):
                b1 = self.boxes[i]
                b2 = self.boxes[i+1]

                quads = [
                    [b1[0][:3], b1[1][:3], b2[1][:3], b2[0][:3]],  # side 1
                    [b1[1][:3], b1[2][:3], b2[2][:3], b2[1][:3]],  # side 2
                    [b1[2][:3], b1[3][:3], b2[3][:3], b2[2][:3]],  # side 3
                    [b1[3][:3], b2[3][:3], b2[0][:3], b1[0][:3]],  # side 4 
                ]

                for j, quad in enumerate(quads):
                    # Convert to numpy arrays
                    p0 = np.array(quad[0], dtype=float).reshape(3,)
                    p1 = np.array(quad[1], dtype=float).reshape(3,)
                    p2 = np.array(quad[2], dtype=float).reshape(3,)

                    # compute normal from two edges
                    v1 = p1 - p0
                    v2 = p2 - p1
                    normal = np.cross(v1, v2)
                    norm_len = np.linalg.norm(normal)
                    if norm_len == 0:
                        continue
                    normal = normal / norm_len

                    # create 8 vertices (original 4 and extruded 4)
                    verts = []
                    for vv in quad:
                        verts.append(tuple(np.array(vv, dtype=float).reshape(3,)))
                    for vv in quad:
                        verts.append(tuple((np.array(vv, dtype=float).reshape(3,) + normal * model_thickness)))

                    # faces as lists of 1-based vertex indices
                    # bottom (original) face
                    faces = [[1,2,3,4],
                             # top (extruded) face (note reversed order to keep normal outward)
                             [8,7,6,5],
                             # four side faces
                             [1,5,6,2],
                             [2,6,7,3],
                             [3,7,8,4],
                             [4,8,5,1]]

                    filename = f"panel_s{i}_f{j}.step"
                    self._write_step_file(filename, verts, faces)

        return

    def export_panels_dxf(self, filename_prefix="panel", scale=1.0,
                           layer_name="0", single_file=False):
        """
        Export panels to DXF.

        By default each quadrilateral face between successive boxes is written
        to its own DXF file named ``{prefix}_s<i>_f<j>.dxf``.  If
        ``single_file`` is True, all panels are written to a single
        multi‑entity DXF named ``{prefix}.dxf`` instead.

        The geometric procedure is the same as before: compute the face normal,
        form a local (u,v) basis, project the four corner points and then write
        an R12 LWPOLYLINE.  The output now contains a minimal LAYER table and
        each polyline is assigned to the specified ``layer_name`` which helps
        tools such as Inkscape import correctly.

        Parameters
        ----------
        filename_prefix : str, optional
            Base name used for the output file(s).  When ``single_file`` is
            False this string is extended with section/face suffixes.
        scale : float, optional
            Scale factor applied to the coordinates.
        layer_name : str, optional
            DXF layer on which the polylines will be placed (default ``"0"``).
        single_file : bool, optional
            Write everything to a single DXF rather than separate files.
        """
        if self.num_sections <= 1:
            return

        panels = []  # list of (verts2d, layer)
        for i in range(len(self.boxes) - 1):
            b1 = self.boxes[i]
            b2 = self.boxes[i + 1]

            quads = [
                [b1[0][:3], b1[1][:3], b2[1][:3], b2[0][:3]],
                [b1[1][:3], b1[2][:3], b2[2][:3], b2[1][:3]],
                [b1[2][:3], b1[3][:3], b2[3][:3], b2[2][:3]],
                [b1[3][:3], b2[3][:3], b2[0][:3], b1[0][:3]],
            ]

            for j, quad in enumerate(quads):
                p0 = np.array(quad[0], dtype=float).reshape(3,)
                p1 = np.array(quad[1], dtype=float).reshape(3,)
                p2 = np.array(quad[2], dtype=float).reshape(3,)

                v1 = p1 - p0
                v2 = p2 - p1
                normal = np.cross(v1, v2)
                norm_len = np.linalg.norm(normal)
                if norm_len == 0:
                    continue
                normal = normal / norm_len

                if abs(normal[0]) < 0.9:
                    ref = np.array([1.0, 0.0, 0.0])
                else:
                    ref = np.array([0.0, 1.0, 0.0])
                u = np.cross(ref, normal)
                u /= np.linalg.norm(u)
                v = np.cross(normal, u)

                verts2d = []
                for vv in quad:
                    p = np.array(vv, dtype=float).reshape(3,)
                    x = np.dot(p, u) * scale
                    y = np.dot(p, v) * scale
                    verts2d.append((x, y))

                panels.append((verts2d, layer_name))

                if not single_file:
                    filename = f"{filename_prefix}_s{i}_f{j}.dxf"
                    self._write_dxf_file(filename, verts2d, layer_name)

        if single_file and panels:
            filename = f"{filename_prefix}.dxf"
            self._write_dxf_file(filename, [v for v, _ in panels], layer_name)

        return

    def _write_dxf_file(self, filename, verts2d, layer_name="0"):
        """
        Write a minimal ASCII DXF (R12) containing one or more closed polylines.

        Parameters
        ----------
        filename : str
            Output path for the DXF file.
        verts2d : list of (float, float) or list of lists
            If a single polyline is desired, provide a list of (x,y) pairs.  If
            multiple polylines are required (single‑file export) pass a list of
            such lists.
        layer_name : str, optional
            Name of the layer to assign to every polyline (default ``"0"``).
        """
        # normalize input to list of polylines
        if verts2d and not isinstance(verts2d[0][0], (list, tuple)):
            polylines = [verts2d]
        else:
            polylines = verts2d

        lines = []
        # header
        lines.extend(["0", "SECTION", "2", "HEADER", "0", "ENDSEC"])

        # minimal layer table
        lines.extend([
            "0", "SECTION", "2", "TABLES",
            "0", "TABLE", "2", "LAYER",
            "0", "LAYER", "2", layer_name,
            "70", "0",       # flags
            "62", "7",       # color (white)
            "6", "CONTINUOUS",  # line type
            "0", "ENDTAB",
            "0", "ENDSEC",
        ])

        # entities
        lines.extend(["0", "SECTION", "2", "ENTITIES"])
        for poly in polylines:
            lines.append("0")
            lines.append("LWPOLYLINE")
            lines.append("8")
            lines.append(layer_name)
            lines.append("90")
            lines.append(str(len(poly)))
            lines.append("70")
            lines.append("1")            # closed
            for x, y in poly:
                lines.append("10")
                lines.append(f"{x:.6f}")
                lines.append("20")
                lines.append(f"{y:.6f}")
        lines.extend(["0", "ENDSEC", "0", "EOF"])

        with open(filename, "w") as fh:
            fh.write("\n".join(lines))
        return


    def _write_step_file(self, filename, vertices, faces):
        """
        Write a valid STEP AP214 file that can be opened in PrusaSlicer.
        
        Args:
            filename: Output file path (e.g., 'output.step')
            vertices: List of (x, y, z) tuples
            faces: List of lists containing 1-based vertex indices
        
        Returns:
            None (writes file to disk)
        """
        lines = []
        
        # ========== HEADER ==========
        lines.append("ISO-10303-21;")
        lines.append("HEADER;")
        lines.append("FILE_DESCRIPTION(('STEP AP214'),'2;1');")
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        lines.append(f"FILE_NAME('{filename}','{timestamp}',(''),(''),'','Python STEP Exporter','');")
        lines.append("FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));")
        lines.append("ENDSEC;")
        lines.append("DATA;")
        
        ent_counter = 1
        
        # ========== APPLICATION CONTEXT & PRODUCT STRUCTURE ==========
        lines.append(f"#{ent_counter}=APPLICATION_CONTEXT('automotive design');")
        app_context_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=APPLICATION_PROTOCOL_DEFINITION('','automotive_design',2001,#{app_context_id});")
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=PRODUCT('Part','Part',$,(#{app_context_id}));")
        product_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=PRODUCT_DEFINITION_FORMATION('','',#{product_id});")
        pdf_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=PRODUCT_DEFINITION_CONTEXT('',#{app_context_id},'design');")
        pdc_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=PRODUCT_DEFINITION('','',#{pdf_id},#{pdc_id});")
        pd_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=PRODUCT_DEFINITION_SHAPE('','',#{pd_id});")
        pds_id = ent_counter
        ent_counter += 1
        
        # ========== GEOMETRIC REPRESENTATION CONTEXT ==========
        lines.append(f"#{ent_counter}=(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.));")
        length_unit_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=(NAMED_UNIT(*)PLANE_ANGLE_UNIT()SI_UNIT($,.RADIAN.));")
        angle_unit_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=(NAMED_UNIT(*)SI_UNIT($,.STERADIAN.)SOLID_ANGLE_UNIT());")
        solid_angle_unit_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-06),#{length_unit_id},'distance_accuracy_value','');")
        uncertainty_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=(GEOMETRIC_REPRESENTATION_CONTEXT(3)GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{uncertainty_id}))GLOBAL_UNIT_ASSIGNED_CONTEXT((#{length_unit_id},#{angle_unit_id},#{solid_angle_unit_id}))REPRESENTATION_CONTEXT('',''));")
        geo_context_id = ent_counter
        ent_counter += 1
        
        # ========== AXIS PLACEMENT (Origin) ==========
        lines.append(f"#{ent_counter}=CARTESIAN_POINT('',(0.,0.,0.));")
        origin_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=DIRECTION('',(0.,0.,1.));")
        z_dir_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=DIRECTION('',(1.,0.,0.));")
        x_dir_id = ent_counter
        ent_counter += 1
        
        lines.append(f"#{ent_counter}=AXIS2_PLACEMENT_3D('',#{origin_id},#{z_dir_id},#{x_dir_id});")
        axis_placement_id = ent_counter
        ent_counter += 1
        
        # ========== GEOMETRY: VERTICES ==========
        cp_ids = []
        vp_ids = []
        for v in vertices:
            x, y, z = float(v[0]), float(v[1]), float(v[2])
            lines.append(f"#{ent_counter}=CARTESIAN_POINT('',({x:.6f},{y:.6f},{z:.6f}));")
            cp_ids.append(ent_counter)
            ent_counter += 1
            
            lines.append(f"#{ent_counter}=VERTEX_POINT('',#{cp_ids[-1]});")
            vp_ids.append(ent_counter)
            ent_counter += 1
        
        # ========== GEOMETRY: EDGES ==========
        edge_data = []
        
        for face_idx, f in enumerate(faces):
            face_edges = []
            num_vertices = len(f)
            
            for i in range(num_vertices):
                v1_idx = f[i] - 1  # Convert from 1-based to 0-based
                v2_idx = f[(i + 1) % num_vertices] - 1
                
                v1_id = vp_ids[v1_idx]
                v2_id = vp_ids[v2_idx]
                
                # Create LINE for the edge
                lines.append(f"#{ent_counter}=CARTESIAN_POINT('',({vertices[v1_idx][0]:.6f},{vertices[v1_idx][1]:.6f},{vertices[v1_idx][2]:.6f}));")
                line_start_id = ent_counter
                ent_counter += 1
                
                # Direction vector
                dx = vertices[v2_idx][0] - vertices[v1_idx][0]
                dy = vertices[v2_idx][1] - vertices[v1_idx][1]
                dz = vertices[v2_idx][2] - vertices[v1_idx][2]
                length = (dx**2 + dy**2 + dz**2)**0.5
                if length > 0:
                    dx, dy, dz = dx/length, dy/length, dz/length
                
                lines.append(f"#{ent_counter}=DIRECTION('',({dx:.6f},{dy:.6f},{dz:.6f}));")
                dir_id = ent_counter
                ent_counter += 1
                
                lines.append(f"#{ent_counter}=VECTOR('',#{dir_id},{length:.6f});")
                vector_id = ent_counter
                ent_counter += 1
                
                lines.append(f"#{ent_counter}=LINE('',#{line_start_id},#{vector_id});")
                line_id = ent_counter
                ent_counter += 1
                
                # EDGE_CURVE
                lines.append(f"#{ent_counter}=EDGE_CURVE('',#{v1_id},#{v2_id},#{line_id},.T.);")
                edge_id = ent_counter
                ent_counter += 1
                
                face_edges.append(edge_id)
            
            edge_data.append(face_edges)
        
        # ========== GEOMETRY: FACES ==========
        face_ids = []
        
        for face_idx, (f, edges) in enumerate(zip(faces, edge_data)):
            # Create ORIENTED_EDGEs
            oriented_edge_ids = []
            for edge_id in edges:
                lines.append(f"#{ent_counter}=ORIENTED_EDGE('',*,*,#{edge_id},.T.);")
                oriented_edge_ids.append(ent_counter)
                ent_counter += 1
            
            # EDGE_LOOP
            edge_refs = ",".join(f"#{oe_id}" for oe_id in oriented_edge_ids)
            lines.append(f"#{ent_counter}=EDGE_LOOP('',({edge_refs}));")
            loop_id = ent_counter
            ent_counter += 1
            
            # FACE_OUTER_BOUND
            lines.append(f"#{ent_counter}=FACE_OUTER_BOUND('',#{loop_id},.T.);")
            bound_id = ent_counter
            ent_counter += 1
            
            # Calculate face normal for PLANE definition
            v0 = vertices[f[0]-1]
            v1 = vertices[f[1]-1]
            v2 = vertices[f[2]-1]
            
            # Two edge vectors
            e1 = [v1[i] - v0[i] for i in range(3)]
            e2 = [v2[i] - v0[i] for i in range(3)]
            
            # Cross product for normal
            nx = e1[1]*e2[2] - e1[2]*e2[1]
            ny = e1[2]*e2[0] - e1[0]*e2[2]
            nz = e1[0]*e2[1] - e1[1]*e2[0]
            n_len = (nx**2 + ny**2 + nz**2)**0.5
            if n_len > 0:
                nx, ny, nz = nx/n_len, ny/n_len, nz/n_len
            
            # PLANE location (use first vertex of face)
            lines.append(f"#{ent_counter}=CARTESIAN_POINT('',({v0[0]:.6f},{v0[1]:.6f},{v0[2]:.6f}));")
            plane_origin_id = ent_counter
            ent_counter += 1
            
            lines.append(f"#{ent_counter}=DIRECTION('',({nx:.6f},{ny:.6f},{nz:.6f}));")
            normal_dir_id = ent_counter
            ent_counter += 1
            
            # Reference direction (perpendicular to normal)
            if abs(nx) < 0.9:
                rx, ry, rz = 1., 0., 0.
            else:
                rx, ry, rz = 0., 1., 0.
            # Make it perpendicular to normal
            dot = rx*nx + ry*ny + rz*nz
            rx -= dot*nx
            ry -= dot*ny
            rz -= dot*nz
            r_len = (rx**2 + ry**2 + rz**2)**0.5
            if r_len > 0:
                rx, ry, rz = rx/r_len, ry/r_len, rz/r_len
            
            lines.append(f"#{ent_counter}=DIRECTION('',({rx:.6f},{ry:.6f},{rz:.6f}));")
            ref_dir_id = ent_counter
            ent_counter += 1
            
            lines.append(f"#{ent_counter}=AXIS2_PLACEMENT_3D('',#{plane_origin_id},#{normal_dir_id},#{ref_dir_id});")
            plane_axis_id = ent_counter
            ent_counter += 1
            
            lines.append(f"#{ent_counter}=PLANE('',#{plane_axis_id});")
            plane_id = ent_counter
            ent_counter += 1
            
            # ADVANCED_FACE
            lines.append(f"#{ent_counter}=ADVANCED_FACE('',(#{bound_id}),#{plane_id},.T.);")
            face_ids.append(ent_counter)
            ent_counter += 1
        
        # ========== CLOSED_SHELL ==========
        face_list = ",".join(f"#{fid}" for fid in face_ids)
        lines.append(f"#{ent_counter}=CLOSED_SHELL('',({face_list}));")
        shell_id = ent_counter
        ent_counter += 1
        
        # ========== MANIFOLD_SOLID_BREP ==========
        lines.append(f"#{ent_counter}=MANIFOLD_SOLID_BREP('',#{shell_id});")
        brep_id = ent_counter
        ent_counter += 1
        
        # ========== SHAPE REPRESENTATION ==========
        lines.append(f"#{ent_counter}=SHAPE_REPRESENTATION('',(#{axis_placement_id},#{brep_id}),#{geo_context_id});")
        shape_rep_id = ent_counter
        ent_counter += 1
        
        # ========== SHAPE DEFINITION REPRESENTATION ==========
        lines.append(f"#{ent_counter}=SHAPE_DEFINITION_REPRESENTATION(#{pds_id},#{shape_rep_id});")
        ent_counter += 1
        
        # ========== END ==========
        lines.append("ENDSEC;")
        lines.append("END-ISO-10303-21;")
        
        with open(filename, "w") as fh:
            fh.write("\n".join(lines))
        
        return

    def get_Polys(self, axis, alpha):

            boxes = []
            base = np.array([self.corner_frame_f(0, 1, 1, alpha).flatten(),
                                self.corner_frame_f(0, 2, 1, alpha).flatten(),
                                self.corner_frame_f(0, 3, 1, alpha).flatten(),
                                self.corner_frame_f(0, 4, 1, alpha).flatten()])

            second_set = np.array([self.corner_frame_f(1, 1, 1, alpha).flatten(),
                                    self.corner_frame_f(1, 2, 1, alpha).flatten(),
                                    self.corner_frame_f(1, 3, 1, alpha).flatten(),
                                    self.corner_frame_f(1, 4, 1, alpha).flatten()])

            boxes.append(base)
            boxes.append(second_set)
            # keep a template of the most-recent box in case other strategies use it
            self.template = second_set.copy()

            for j in range(2, self.num_sections):
                new_box = np.array([self.corner_frame_f(j, 1, 1, alpha).flatten(),
                                    self.corner_frame_f(j, 2, 1, alpha).flatten(),
                                    self.corner_frame_f(j, 3, 1, alpha).flatten(),
                                    self.corner_frame_f(j, 4, 1, alpha).flatten()])
                boxes.append(new_box)

            # fig = plt.figure()
            # ax = plt.axes(projection="3d")


            color_counter = 0
            # Plotting the boxes
            if self.num_sections > 1:
                for i in range(len(boxes)-1):
                    if color_counter > 2:
                        color_counter = 0
                    b1 = boxes[i]
                    b2 = boxes[i+1]

                    # build 6 faces
                    faces = [
                        [b1[0][:3], b1[1][:3], b2[1][:3], b2[0][:3]],  # side 1
                        [b1[1][:3], b1[2][:3], b2[2][:3], b2[1][:3]],  # side 2
                        [b1[2][:3], b1[3][:3], b2[3][:3], b2[2][:3]],  # side 3
                        [b1[3][:3], b2[3][:3], b2[0][:3], b1[0][:3]],  # side 4 
                        [b1[0][:3], b1[1][:3], b1[2][:3], b1[3][:3]],  # bottom
                        [b2[0][:3], b2[1][:3], b2[2][:3], b2[3][:3]]   # top
                    ]
                    axis.add_collection3d(Poly3DCollection(faces, alpha=0.8, facecolor = self.color_list[color_counter], edgecolor = "black"))
                    color_counter += 1

            return

    def show_animation(self):
        """
        A function that shows an animation of the tube folding up.
        """

        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation

        fig = plt.figure()
        ax = plt.axes(projection="3d")


        def animate(i):
            ax.clear()
            ax.set_xlim([-4*self.width, 4*self.width])
            ax.set_ylim([-4*self.width, 4*self.width])
            ax.set_zlim([-4*self.height, 4*self.height])

            ax.plot([0, 2], [0, 0], [0, 0], color='r')
            ax.plot([0, 0], [0, 2], [0, 0], color='g')
            ax.plot([0, 0], [0, 0], [0, 2], color='b')

            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")

            
            if i < 180:
                alpha = i / 2
            else:
                alpha = (360 - i) / 2

            self.get_Polys(axis=ax, alpha = np.radians(alpha))


        anim = FuncAnimation(fig, animate, frames=360, interval=50)

        plt.show()
        # anim.save('tube_animation.gif')





        return
    
    def line_to_tube(self, num_sections):
        """
        A function that takes in a line and outputs the corresponding tube.
        """

        return
        
        
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
        return