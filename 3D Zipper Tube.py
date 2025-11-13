import numpy as np


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

# the individual matrix function has been verified:
def individual_matrix(alpha, L_f, theta_f, gamma_f):
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

def corner_frame_s(n, L_s, theta_s, gamma_s):
    c_s_1_s = np.array([[0],
                        [L_s],
                        [0]])
    c_s_2_s = np.array([[w],
                        [L_s - w*cot(gamma_s)],
                        [0]])
    c_s_3_s = np.array([[w + h*cos(alpha)],
                        [L_s - w*cot(gamma_s) - h*cot(theta_s)],
                        [h*sin(alpha)]])
    c_s_4_s = np.array([[h*cos(alpha)],
                        [L_s - h*cot(theta_s)],
                        [h*sin(alpha)]])
    if n == 1:
        return c_s_1_s
    elif n == 2:
        return c_s_2_s
    elif n == 3:
        return c_s_3_s
    elif n == 4:
        return c_s_4_s



if __name__ == '__main__':
    # Testing:
    alpha = np.radians(60)  # must be between 0 and 180 degrees
    h = 5
    w = 10

    # Segment 0 parameters:
    theta_0 = np.radians(60)
    gamma_0 = np.radians(70)

    # Segment 1 parameters:
    L_1 = 15
    theta_1 = np.radians(30)
    gamma_1 = np.radians(120)

    # Segment 2 parameters:
    L_2 = 25
    theta_2 = np.radians(50)
    gamma_2 = np.radians(60)

    # Segment 3 parrameters:
    L_3 = 20
    theta_3 = np.radians(110)
    gamma_3 = np.radians(45)

    T = individual_matrix(alpha, L_1, theta_1, gamma_1)
    print(T)