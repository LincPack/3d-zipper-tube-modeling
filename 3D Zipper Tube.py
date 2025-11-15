import numpy as np
from commctrl import LVM_SETITEMPOSITION32

# INSTRUCTIONS FOR USING CODE:
'''Put instructions here later'''

# Define all parameters here:
# Parameters pertinent to every segment in every frame:
h = 5
w = 10
alpha = np.radians(60)

# Parameters for Segment 0:
# L_0 doesn't exist, but there will be a length for every other segment.
theta_0 = np.radians(60)
gamma_0 = np.radians(70)

# Parameters for Segment 1:
L_1 = 15
theta_1 = np.radians(30)
gamma_1 = np.radians(120)

# Parameters for Segment 2:
L_2 = 25
theta_2 = np.radians(50)
gamma_2 = np.radians(60)

# Parameters for Segment 3:
L_3 = 20
theta_3 = np.radians(110)
gamma_3 = np.radians(45)

# The following functions aren't really necessary, but they make the coding faster and easier to read:
def cos(angle):
    return np.cos(angle)

def sin(angle):
    return np.sin(angle)

def tan(angle):
    return np.tan(angle)

def csc(angle):
    return 1/np.sin(angle)

def cot(angle):
    return 1/np.tan(angle)

# Define the coordinates of the corners of Segment 0 (see visuals in paper to understand which corners these refer to):
c_0_1_1 = np.array([[0],
                    [0],
                    [0]])
c_0_2_1 = np.array([[w],
                    [-w*cot(gamma_0)],
                    [0]])
c_0_3_1 = np.array([[w + h*cos(alpha)],
                    [-w*cot(gamma_0) - h*cot(theta_0)],
                    [h*sin(alpha)]])
c_0_4_1 = np.array([[h*cos(alpha)],
                    [-h*cot(theta_0)],
                    [h*sin(alpha)]])

def corner_frame_s(s, n):
    L_s = parameters[0][s]
    theta_s = parameters[1][s]
    gamma_s = parameters[2][s]

    if n == 1:
        c_s_1_s = np.array([[0],
                            [L_s],
                            [0]])
        return c_s_1_s
    elif n == 2:
        c_s_2_s = np.array([[w],
                            [L_s - w * cot(gamma_s)],
                            [0]])
        return c_s_2_s
    elif n == 3:
        c_s_3_s = np.array([[w + h * cos(alpha)],
                            [L_s - w * cot(gamma_s) - h * cot(theta_s)],
                            [h * sin(alpha)]])
        return c_s_3_s
    elif n == 4:
        c_s_4_s = np.array([[h * cos(alpha)],
                            [L_s - h * cot(theta_s)],
                            [h * sin(alpha)]])
        return c_s_4_s

# the individual matrix function has been verified:
def individual_matrix(L_f, theta_f, gamma_f):
    # this function returns T_f,f+1 for a given frame
    u_f = cot(theta_f) - cos(alpha) * cot(gamma_f)
    a_f = csc(gamma_f)
    b_f = np.sqrt((cot(gamma_f) - cot(theta_f) * cos(alpha)) ** 2 + (sin(alpha) * csc(theta_f)) ** 2)
    c_f = a_f * np.sqrt(u_f ** 2 + (sin(alpha) * csc(gamma_f)) ** 2)
    d_f = np.sqrt(((sin(alpha) / b_f) ** 2 + (u_f / c_f) ** 2) ** 2 + (cos(gamma_f) * sin(alpha) / b_f) ** 2 + (
                u_f * cos(gamma_f) / c_f) ** 2)
    m_f = np.sqrt(cos(gamma_f) ** 2 + (sin(alpha) / b_f) ** 2 + (u_f / c_f) ** 2)
    g_f = np.sqrt((u_f / c_f) ** 2 + (sin(alpha) / b_f) ** 2)
    q_f = sin(alpha) * cos(gamma_f)
    r_f = sin(alpha) * cot(gamma_f)
    T_individual = np.array([[1/d_f*(((sin(alpha)/b_f)**2 + (u_f/c_f)**2)/a_f - r_f*q_f/b_f**2 + u_f**2*cot(gamma_f)*cos(gamma_f)/c_f**2), 1/m_f*(cos(gamma_f)/a_f + r_f*sin(alpha)/b_f**2 - u_f**2*cot(gamma_f)/c_f**2), -2*u_f*r_f/(b_f*c_f*g_f), 0],
                             [-1/d_f*(cot(gamma_f)*((sin(alpha)/b_f)**2 - (u_f/c_f)**2)/a_f + q_f*sin(alpha)/b_f**2 + u_f**2*cos(gamma_f)/c_f**2), 1/m_f*(sin(alpha)**2/b_f**2 - cot(gamma_f)*cos(gamma_f)/a_f - u_f**2/c_f**2), -2*u_f*sin(alpha)/(b_f*c_f*g_f), L_f],
                             [-u_f*q_f/d_f*(a_f**2/c_f**2 + 1/b_f**2), u_f*sin(alpha)/m_f*(1/b_f**2 + a_f**2/c_f**2), 1/(b_f*c_f*g_f)*(-u_f**2 + a_f**2*sin(alpha)**2), 0],
                             [0, 0, 0, 1]])
    return T_individual

def combined_matrix(parameter_list, s, f):
    # Make the parameter list such that parameters for segment 1 are in the second column
    L_list = parameter_list[0]
    theta_list = parameter_list[1]
    gamma_list = parameter_list[2]

    # Create list of arrays. Each array represents a matrix that transforms from one frame to the next immediate frame.
    T_list = [0]
    i = f
    while i <= s - 1:
        T_i = individual_matrix(L_list[i], theta_list[i], gamma_list[i])
        T_list.append(T_i)
        i += 1

    # Matrix multiplication by mapping:
    i = f
    T_product = T_list[i]
    while i < s - 1:
        T_product = T_product @ T_list[i+1]
        i += 1
    T_combined = T_product

    return T_combined

def corner_frame_f(s, n, f):
    T = combined_matrix(parameters, s, f)
    c_s_n_s = np.append(corner_frame_s(s,n), np.array([[1]]), axis = 0)
    c_s_n_f = np.delete(T @ c_s_n_s, 3, axis=0)
    return c_s_n_f

if __name__ == '__main__':
    # Testing:
    #   Verified:
    #       c_0_n_1 coordinates
    #       individual_matrix
    #       corner_frame_s verified

    parameters = [[0, L_1, L_2, L_3],
                  [theta_0, theta_1, theta_2, theta_3],
                  [gamma_0, gamma_1, gamma_2, gamma_3]]

    print(np.append(corner_frame_s(3,4), np.array([[1]]), axis = 0))

    c_3_1_1 = corner_frame_f(3, 1, 1)
    c_3_2_1 = corner_frame_f(3, 2, 1)
    c_3_3_1 = corner_frame_f(3, 3, 1)
    c_3_4_1 = corner_frame_f(3, 4, 1)

    print(c_3_1_1)
    print(c_3_2_1)
    print(c_3_3_1)
    print(c_3_4_1)

