import numpy as np
# from commctrl import LVM_SETITEMPOSITION32

# INSTRUCTIONS FOR USING CODE:
'''Put instructions here later'''

# Parameters pertinent to every segment in every frame:
h = 5
w = 10
alpha = np.radians(60)
# The parameters for each individual segment are defined under "if __name__ == '__main__':".


# The following trigonometric functions make the coding faster and easier to read:
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


# This function returns the corner coordinate for corner type n in the same frame as the segment. c_s_n_s:
def corner_frame_s(s, n):
    L_s = parameters[0][s]
    theta_s = parameters[1][s]
    gamma_s = parameters[2][s]

    if n == 1:
        c_s_n_s = np.array([[0],
                            [L_s],
                            [0]])
        return c_s_n_s
    elif n == 2:
        c_s_n_s = np.array([[w],
                            [L_s - w * cot(gamma_s)],
                            [0]])
        return c_s_n_s
    elif n == 3:
        c_s_n_s = np.array([[w + h * cos(alpha)],
                            [L_s - w * cot(gamma_s) - h * cot(theta_s)],
                            [h * sin(alpha)]])
        return c_s_n_s
    elif n == 4:
        c_s_n_s = np.array([[h * cos(alpha)],
                            [L_s - h * cot(theta_s)],
                            [h * sin(alpha)]])
        return c_s_n_s


# This function returns the matrix needed to transform between two immediate coordinate frames. In the paper, this matrix is called T_f,f+1:
def individual_matrix(L_f, theta_f, gamma_f):
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


# This function returns the product of all individual matrices needed to transform the corner coordinates in frame s to frame f, resulting in one matrix that will be multiplied by c_s_n_s:
def combined_matrix(parameter_list, s, f):
    # Make the parameter list such that parameters for segment 1 are in the second column
    L_list = parameter_list[0]
    theta_list = parameter_list[1]
    gamma_list = parameter_list[2]

    # Create list of arrays. Each array represents a matrix that transforms from one frame to the next immediate frame.
    T_list = []
    i = f
    while i <= s - 1:
        T_i = individual_matrix(L_list[i], theta_list[i], gamma_list[i])
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
def corner_frame_f(s, n, f):
    if s == 0 and f == 1:
        if n == 1:
            c_s_n_f = np.array([[0],
                                [0],
                                [0]])
            return c_s_n_f
        elif n == 2:
            c_s_n_f = np.array([[w],
                                [-w*cot(gamma_0)],
                                [0]])
            return c_s_n_f
        elif n == 3:
            c_s_n_f = np.array([[w + h*cos(alpha)],
                                [-w*cot(gamma_0) - h*cot(theta_0)],
                                [h*sin(alpha)]])
            return c_s_n_f
        elif n == 4:
            c_s_n_f = np.array([[h*cos(alpha)],
                                [-h*cot(theta_0)],
                                [h*sin(alpha)]])
            return c_s_n_f
    elif s == f:
        c_s_n_f = corner_frame_s(s, n)
        return c_s_n_f
    elif s > f:
        T = combined_matrix(parameters, s, f)
        c_s_n_s = np.append(corner_frame_s(s,n), np.array([[1]]), axis = 0)
        c_s_n_f = np.delete(T @ c_s_n_s, 3, axis=0)
        return c_s_n_f
    else:
        return "This code does not support situations when s < f. Please choose a frame that corresponds to your chosen segment or is less far down the tube than the segment. In other word, the condition s >= f must be true. An exception is when s = 0 and f = 1. These coordinates can be calculated if desired."


if __name__ == '__main__':

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

    parameters = [[0, L_1, L_2, L_3],
                  [theta_0, theta_1, theta_2, theta_3],
                  [gamma_0, gamma_1, gamma_2, gamma_3]]

    # Frame 1:
    c_0_1_1 = corner_frame_f(0, 1, 1)
    c_0_2_1 = corner_frame_f(0, 2, 1)
    c_0_3_1 = corner_frame_f(0, 3, 1)
    c_0_4_1 = corner_frame_f(0, 4, 1)

    c_1_1_1 = corner_frame_f(1, 1, 1)
    c_1_2_1 = corner_frame_f(1, 2, 1)
    c_1_3_1 = corner_frame_f(1, 3, 1)
    c_1_4_1 = corner_frame_f(1, 4, 1)

    c_2_1_1 = corner_frame_f(2, 1, 1)
    c_2_2_1 = corner_frame_f(2, 2, 1)
    c_2_3_1 = corner_frame_f(2, 3, 1)
    c_2_4_1 = corner_frame_f(2, 4, 1)

    c_3_1_1 = corner_frame_f(3, 1, 1)
    c_3_2_1 = corner_frame_f(3, 2, 1)
    c_3_3_1 = corner_frame_f(3, 3, 1)
    c_3_4_1 = corner_frame_f(3, 4, 1)

    # Frame 2:
    c_0_1_2 = corner_frame_f(0, 1, 2)
    c_0_2_2 = corner_frame_f(0, 2, 2)
    c_0_3_2 = corner_frame_f(0, 3, 2)
    c_0_4_2 = corner_frame_f(0, 4, 2)

    c_1_1_2 = corner_frame_f(1, 1, 2)
    c_1_2_2 = corner_frame_f(1, 2, 2)
    c_1_3_2 = corner_frame_f(1, 3, 2)
    c_1_4_2 = corner_frame_f(1, 4, 2)

    c_2_1_2 = corner_frame_f(2, 1, 2)
    c_2_2_2 = corner_frame_f(2, 2, 2)
    c_2_3_2 = corner_frame_f(2, 3, 2)
    c_2_4_2 = corner_frame_f(2, 4, 2)

    c_3_1_2 = corner_frame_f(3, 1, 2)
    c_3_2_2 = corner_frame_f(3, 2, 2)
    c_3_3_2 = corner_frame_f(3, 3, 2)
    c_3_4_2 = corner_frame_f(3, 4, 2)

    # Frame 3:
    c_0_1_3 = corner_frame_f(0, 1, 3)
    c_0_2_3 = corner_frame_f(0, 2, 3)
    c_0_3_3 = corner_frame_f(0, 3, 3)
    c_0_4_3 = corner_frame_f(0, 4, 3)

    c_1_1_3 = corner_frame_f(1, 1, 3)
    c_1_2_3 = corner_frame_f(1, 2, 3)
    c_1_3_3 = corner_frame_f(1, 3, 3)
    c_1_4_3 = corner_frame_f(1, 4, 3)

    c_2_1_3 = corner_frame_f(2, 1, 3)
    c_2_2_3 = corner_frame_f(2, 2, 3)
    c_2_3_3 = corner_frame_f(2, 3, 3)
    c_2_4_3 = corner_frame_f(2, 4, 3)

    c_3_1_3 = corner_frame_f(3, 1, 3)
    c_3_2_3 = corner_frame_f(3, 2, 3)
    c_3_3_3 = corner_frame_f(3, 3, 3)
    c_3_4_3 = corner_frame_f(3, 4, 3)

    print('Frame 1:')
    # Segment 0 in Frame 1 looks the prettiest when printed. If you want the other coordinates to look like this, you could use the same approach or incorporate cleaning up the coordinates in a function
    print(' Segment 0:')
    print(f'        c_0,1,1 = {c_0_1_1[0][0].round(2), c_0_1_1[1][0].round(2), c_0_1_1[2][0].round(2)}')
    print(f'        c_0,2,1 = {c_0_2_1[0][0].round(2), c_0_2_1[1][0].round(2), c_0_2_1[2][0].round(2)}')
    print(f'        c_0,3,1 = {c_0_3_1[0][0].round(2), c_0_3_1[1][0].round(2), c_0_3_1[2][0].round(2)}')
    print(f'        c_0,4,1 = {c_0_4_1[0][0].round(2), c_0_4_1[1][0].round(2), c_0_4_1[2][0].round(2)}\n')

    print(' Segment 1:')
    print(f'        c_1,1,1 = {c_1_1_1}')
    print(f'        c_1,2,1 = {c_1_2_1}')
    print(f'        c_1,3,1 = {c_1_3_1}')
    print(f'        c_1,4,1 = {c_1_4_1}\n')

    print(' Segment 2:')
    print(f'        c_2,1,1 = {c_2_1_1}')
    print(f'        c_2,2,1 = {c_2_2_1}')
    print(f'        c_2,3,1 = {c_2_3_1}')
    print(f'        c_2,4,1 = {c_2_4_1}\n')

    print(' Segment 3:')
    print(f'        c_3,1,1 = {c_3_1_1}')
    print(f'        c_3,2,1 = {c_3_2_1}')
    print(f'        c_3,3,1 = {c_3_3_1}')
    print(f'        c_3,4,1 = {c_3_4_1}\n')

    print('Frame 2:')
    print(' Segment 1:')
    print(f'        c_1,1,2 = {c_1_1_2}')
    print(f'        c_1,2,2 = {c_1_2_2}')
    print(f'        c_1,3,2 = {c_1_3_2}')
    print(f'        c_1,4,2 = {c_1_4_2}\n')

    print(' Segment 2:')
    print(f'        c_2,1,2 = {c_2_1_2}')
    print(f'        c_2,2,2 = {c_2_2_2}')
    print(f'        c_2,3,2 = {c_2_3_2}')
    print(f'        c_2,4,2 = {c_2_4_2}\n')

    print(' Segment 3:')
    print(f'        c_3,1,2 = {c_3_1_2}')
    print(f'        c_3,2,2 = {c_3_2_2}')
    print(f'        c_3,3,2 = {c_3_3_2}')
    print(f'        c_3,4,2 = {c_3_4_2}\n')

    print('Frame 3:')
    print(' Segment 3:')
    print(f'        c_3,1,3 = {c_3_1_3}')
    print(f'        c_3,2,3 = {c_3_2_3}')
    print(f'        c_3,3,3 = {c_3_3_3}')
    print(f'        c_3,4,3 = {c_3_4_3}\n')