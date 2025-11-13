import numpy as np

# Parameters that apply to the whole tube:
alpha = np.radians(60) # must be between 0 and 180 degrees
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

u_1 = cot(theta_1) - cos(alpha)*cot(gamma_1)
a_1 = csc(gamma_1)
b_1 = np.sqrt((cot(gamma_1) - cot(theta_1)*cos(alpha))**2 + (sin(alpha)*csc(theta_1))**2)
c_1 = a_1*np.sqrt(u_1**2 + (sin(alpha)*csc(gamma_1))**2)
d_1 = np.sqrt(((sin(alpha)/b_1)**2 + (u_1/c_1)**2)**2 + (cos(gamma_1)*sin(alpha)/b_1)**2 + (u_1*cos(gamma_1)/c_1)**2)
m_1 = np.sqrt(cos(gamma_1)**2 + (sin(alpha)/b_1)**2 + (u_1/c_1)**2)
g_1 = np.sqrt((u_1/c_1)**2 + (sin(alpha)/b_1)**2)
q_1 = sin(alpha)*cos(gamma_1)
r_1 = sin(alpha)*cot(gamma_1)

'''b = np.sqrt((cot(gamma_1) - cot(theta_1)*cos(alpha))**2 + (sin(alpha)*csc(theta_1))**2)
c = csc(gamma_1)*np.sqrt((cot(gamma_1)*cos(alpha) - cot(theta_1))**2 + (sin(alpha)*csc(gamma_1))**2)'''

# Affine Transformations:
# This first matrix has some sign errors which have not been corrected:
'''T_1_2 = np.array([[((sin(alpha)/b)**2 - (u/c)**2)/(a*d) - r*q/(b**2*d) - u**2*cot(gamma_1)*cos(gamma_1)/(c**2*d), cos(gamma_1)/(a*f) + r*sin(alpha)/(b**2*f) - u**2*cot(gamma_1)/(c**2*f), u*r/(b*c*g) + u*r/(b*c*g), 0],
                  [-cot(gamma_1)*((sin(alpha)/b)**2 - (u/c)**2)/(a*d) - q*sin(alpha)/(b**2*d) - u**2*cos(gamma_1)/(c**2*d), -cot(gamma_1)*cos(gamma_1)/(a*f) + sin(alpha)**2/(b**2*f) - u**2/(c**2*f), 0, L_1],
                  [-u*q/(b**2*d) + u*q*a**2/(c**2*d), u*sin(alpha)/(b**2*f) + u*a**2*sin(alpha)/(c**2*f), u**2/(b*c*g) + a**2*sin(alpha)**2/(b*c*g), 0],
                  [0, 0, 0, 1]])
# Verification with TI-84 Plus. The following entries have the same value in code and in the calculator with the given parameters: L_1 = 15; gamma_1 = np.radians(120); alpha = np.radians(60); theta_1 = np.radians(30)
# 11: -0.97484462
# 12: -0.13738195
# 13: -0.34651625
# 14: 0
# 21: 0.16267013
# 22: -0.70100015
# 23: 0
# 24: 15
# 31: -0.07466826
# 32: 0.55522254
# 33: 0.87169546
# 34: 0
# 41, 42, 43, 44 are correct
'''

# The matrix below has been giving me problems for some reason:
'''T_1_2_new = np.array([[1/d*(((sin(alpha)/b)**2 + (u/c)**2)/a - r*q/b**2 + u**2*cot(gamma_1)*cos(gamma_1)/c**2), 1/m*(cos(gamma_1)/a + r*sin(alpha)/b**2 - u**2*cot(gamma_1)/c**2), -2*u*r/(b*c*g), 0],
                  [-1/d*(cot(gamma_1)*((sin(alpha)/b)**2 + (u/c)**2)/a + q*sin(alpha)/b**2 + u**2*cos(gamma_1)/c**2), 1/m*(sin(alpha)**2/b**2 - cot(gamma_1)*cos(gamma_1)/a - u**2/c**2), -2*u*sin(alpha)/(b*c*g), L_1],
                  [-u*q/d*(a**2/c**2 + 1/b**2), u*sin(alpha)/m*(1/b**2 + a**2/c**2), 1/(b*c*g)*(-u**2 + a**2*sin(alpha)**2), 0],
                  [0, 0, 0, 1]])'''

# The matrix below works!
'''T_1_2_new = np.array([[1/d*(((sin(alpha)/b)**2 + (u/c)**2)/a - r*q/b**2 + u**2*cot(gamma_1)*cos(gamma_1)/c**2), 1/m*(cos(gamma_1)/a + r*sin(alpha)/b**2 - u**2*cot(gamma_1)/c**2), -2*u*r/(b*c*g), 0],
                  [-cot(gamma_1)*((sin(alpha)/b)**2 + ((cot(theta_1) - cos(alpha)*cot(gamma_1))/c)**2)/(a*d) - sin(alpha)**2*cos(gamma_1)/(b**2*d) + cos(gamma_1)*(cot(theta_1) - cos(alpha)*cot(gamma_1))**2/(c**2*d), 1/m*(sin(alpha)**2/b**2 - cot(gamma_1)*cos(gamma_1)/a - u**2/c**2), -sin(alpha)*(cot(theta_1) - cos(alpha)*cot(gamma_1))/(b*c*g) + sin(alpha)*(cos(alpha)*cot(gamma_1) - cot(theta_1))/(b*c*g), L_1],
                  [-u*q/d*(a**2/c**2 + 1/b**2), u*sin(alpha)/m*(1/b**2 + a**2/c**2), 1/(b*c*g)*(-u**2 + a**2*sin(alpha)**2), 0],
                  [0, 0, 0, 1]])'''

# This matrix also works:
'''T_1_2_new = np.array([[1/d*(((sin(alpha)/b)**2 + (u/c)**2)/a - r*q/b**2 + u**2*cot(gamma_1)*cos(gamma_1)/c**2), 1/m*(cos(gamma_1)/a + r*sin(alpha)/b**2 - u**2*cot(gamma_1)/c**2), -2*u*r/(b*c*g), 0],
                      [-cot(gamma_1)*((sin(alpha)/b)**2 + (u/c)**2)/(a*d) - sin(alpha)**2*cos(gamma_1)/(b**2*d) + cos(gamma_1)*u**2/(c**2*d), 1/m*(sin(alpha)**2/b**2 - cot(gamma_1)*cos(gamma_1)/a - u**2/c**2), -sin(alpha)*u/(b*c*g) - sin(alpha)*u/(b*c*g), L_1],
                      [-u*q/d*(a**2/c**2 + 1/b**2), u*sin(alpha)/m*(1/b**2 + a**2/c**2), 1/(b*c*g)*(-u**2 + a**2*sin(alpha)**2), 0],
                      [0, 0, 0, 1]])'''

# This matrix also works:
'''T_1_2_new = np.array([[1/d*(((sin(alpha)/b)**2 + (u/c)**2)/a - r*q/b**2 + u**2*cot(gamma_1)*cos(gamma_1)/c**2), 1/m*(cos(gamma_1)/a + r*sin(alpha)/b**2 - u**2*cot(gamma_1)/c**2), -2*u*r/(b*c*g), 0],
                      [-cot(gamma_1)*((sin(alpha)/b)**2 + (u/c)**2)/(a*d) - q*sin(alpha)/(b**2*d) + u**2*cos(gamma_1)/(c**2*d), 1/m*(sin(alpha)**2/b**2 - cot(gamma_1)*cos(gamma_1)/a - u**2/c**2), -2*u*sin(alpha)/(b*c*g), L_1],
                      [-u*q/d*(a**2/c**2 + 1/b**2), u*sin(alpha)/m*(1/b**2 + a**2/c**2), 1/(b*c*g)*(-u**2 + a**2*sin(alpha)**2), 0],
                      [0, 0, 0, 1]])'''

# This is the most simplified T_1,2 matrix that works:
T_1_2_new = np.array([[1/d_1*(((sin(alpha)/b_1)**2 + (u_1/c_1)**2)/a_1 - r_1*q_1/b_1**2 + u_1**2*cot(gamma_1)*cos(gamma_1)/c_1**2), 1/m_1*(cos(gamma_1)/a_1 + r_1*sin(alpha)/b_1**2 - u_1**2*cot(gamma_1)/c_1**2), -2*u_1*r_1/(b_1*c_1*g_1), 0],
                      [-1/d_1*(cot(gamma_1)*((sin(alpha)/b_1)**2 - (u_1/c_1)**2)/a_1 + q_1*sin(alpha)/b_1**2 + u_1**2*cos(gamma_1)/c_1**2), 1/m_1*(sin(alpha)**2/b_1**2 - cot(gamma_1)*cos(gamma_1)/a_1 - u_1**2/c_1**2), -2*u_1*sin(alpha)/(b_1*c_1*g_1), L_1],
                      [-u_1*q_1/d_1*(a_1**2/c_1**2 + 1/b_1**2), u_1*sin(alpha)/m_1*(1/b_1**2 + a_1**2/c_1**2), 1/(b_1*c_1*g_1)*(-u_1**2 + a_1**2*sin(alpha)**2), 0],
                      [0, 0, 0, 1]])

u_2 = cot(theta_2) - cos(alpha)*cot(gamma_2)
a_2 = csc(gamma_2)
b_2 = np.sqrt((cot(gamma_2) - cot(theta_2)*cos(alpha))**2 + (sin(alpha)*csc(theta_2))**2)
c_2 = a_2*np.sqrt(u_2**2 + (sin(alpha)*csc(gamma_2))**2)
d_2 = np.sqrt(((sin(alpha)/b_2)**2 + (u_2/c_2)**2)**2 + (cos(gamma_2)*sin(alpha)/b_2)**2 + (u_2*cos(gamma_2)/c_2)**2)
m_2 = np.sqrt(cos(gamma_2)**2 + (sin(alpha)/b_2)**2 + (u_2/c_2)**2)
g_2 = np.sqrt((u_2/c_2)**2 + (sin(alpha)/b_2)**2)
q_2 = sin(alpha)*cos(gamma_2)
r_2 = sin(alpha)*cot(gamma_2)

T_2_3 = np.array([[1/d_2*(((sin(alpha)/b_2)**2 + (u_2/c_2)**2)/a_2 - r_2*q_2/b_2**2 + u_2**2*cot(gamma_2)*cos(gamma_2)/c_2**2), 1/m_2*(cos(gamma_2)/a_2 + r_2*sin(alpha)/b_2**2 - u_2**2*cot(gamma_2)/c_2**2), -2*u_2*r_2/(b_2*c_2*g_2), 0],
                      [-1/d_2*(cot(gamma_2)*((sin(alpha)/b_2)**2 - (u_2/c_2)**2)/a_2 + q_2*sin(alpha)/b_2**2 + u_2**2*cos(gamma_2)/c_2**2), 1/m_2*(sin(alpha)**2/b_2**2 - cot(gamma_2)*cos(gamma_2)/a_2 - u_2**2/c_2**2), -2*u_2*sin(alpha)/(b_2*c_2*g_2), L_2],
                      [-u_2*q_2/d_2*(a_2**2/c_2**2 + 1/b_2**2), u_2*sin(alpha)/m_2*(1/b_2**2 + a_2**2/c_2**2), 1/(b_2*c_2*g_2)*(-u_2**2 + a_2**2*sin(alpha)**2), 0],
                      [0, 0, 0, 1]])

'''T_1doubleprime_1 = np.array([[1/a, -cot(gamma_1)/a, 0, L_1*cot(gamma_1)/a],
                            [sin(alpha)*cot(gamma_1)/b, sin(alpha)/b, (cot(theta_1) - cos(alpha)*cot(gamma_1))/b, -L_1*sin(alpha)/b],
                            [cot(gamma_1)*(cot(gamma_1)*cos(alpha) - cot(theta_1))/c, (cos(alpha)*cot(gamma_1) - cot(theta_1))/c, (sin(alpha)*csc(gamma_1)**2)/c, -L_1*(cos(alpha)*cot(gamma_1) - cot(theta_1))/c],
                            [0, 0, 0, 1]])'''

# Define points of each segment:
# Segment 0:
C_0_1_1 = np.array([[0],
                    [0],
                    [0],
                    [1]])
C_0_2_1 = np.array([[w],
                    [-w*cot(gamma_0)],
                    [0],
                    [1]])
C_0_3_1 = np.array([[w + h*cos(alpha)],
                    [-w*cot(gamma_0) - h*cot(theta_0)],
                    [h*sin(alpha)],
                    [1]])
C_0_4_1 = np.array([[h*cos(alpha)],
                    [-h*cot(theta_0)],
                    [h*sin(alpha)],
                    [1]])



# Segment 1:
# These points have been verified
C_1_1_1 = np.array([[0],
                    [L_1],
                    [0],
                    [1]])
C_1_2_1 = np.array([[w],
                    [L_1 - w*cot(gamma_1)],
                    [0],
                    [1]])
C_1_3_1 = np.array([[w + h*cos(alpha)],
                    [L_1 - w*cot(gamma_1) - h*cot(theta_1)],
                    [h*sin(alpha)],
                    [1]])
C_1_4_1 = np.array([[h*cos(alpha)],
                    [L_1 - h*cot(theta_1)],
                    [h*sin(alpha)],
                    [1]])

# Segment 2:
# These points have been verified
C_2_1_2 = np.array([[0],
                    [L_2],
                    [0],
                    [1]])
C_2_2_2 = np.array([[w],
                    [L_2 - w*cot(gamma_2)],
                    [0],
                    [1]])
C_2_3_2 = np.array([[w + h*cos(alpha)],
                    [L_2 - w*cot(gamma_2) - h*cot(theta_2)],
                    [h*sin(alpha)],
                    [1]])
C_2_4_2 = np.array([[h*cos(alpha)],
                    [L_2 - h*cot(theta_2)],
                    [h*sin(alpha)],
                    [1]])

# Segment 3:
C_3_1_3 = np.array([[0],
                    [L_3],
                    [0],
                    [1]])
C_3_2_3 = np.array([[w],
                    [L_3 - w*cot(gamma_3)],
                    [0],
                    [1]])
C_3_3_3 = np.array([[w + h*cos(alpha)],
                    [L_3 - w*cot(gamma_3) - h*cot(theta_3)],
                    [h*sin(alpha)],
                    [1]])
C_3_4_3 = np.array([[h*cos(alpha)],
                    [L_3 - h*cot(theta_3)],
                    [h*sin(alpha)],
                    [1]])

# Test the mirroring direction
'''x_2_1doubleprime = np.array([[((sin(alpha)/b)**2 + ((cot(theta_1) - cos(alpha)*cot(gamma_1))/c)**2)/d],
                             [-cos(gamma_1)*sin(alpha)/(b*d)],
                             [-cos(gamma_1)*(cos(theta_1) - cos(alpha)*cot(gamma_1))/(c*d)]])
y_2_1doubleprime = np.array([[cos(gamma_1)/m],
                             [sin(alpha)/(b*m)],
                             [(cot(theta_1) - cos(alpha)*cot(gamma_1))/(c*m)]])
z_2_1doubleprime = np.array([[0],
                             [(-cot(theta_1) + cos(alpha)*cot(gamma_1))/(c*g)],
                             [sin(alpha)/(b*g)]])'''
# There is something wrong with y_2_1doubleprime, which means there is something wrong with the other two unit vectors as well.

# Test C_0_1_1":
'''C_0_1_1doubleprime = np.array([[L_1*cot(gamma_1)/a],
                    [-L_1*sin(alpha)/b],
                    [-L_1*(cos(alpha)*cot(gamma_1) - cot(theta_1))/c]])'''

if __name__ == '__main__':
    '''print(round(L_1*cot(gamma_1)/a, 2))
    print(round(-L_1*sin(alpha)/b, 2))
    print(round(-L_1*(cos(alpha)*cot(gamma_1) - cot(theta_1))/c, 2))'''

    print(f'C_1,1,1 = {C_1_1_1}')
    print(f'C_1,2,1 = {C_1_2_1}')
    print(f'C_1,3,1 = {C_1_3_1}')
    print(f'C_1,4,1 = {C_1_4_1}')

    '''print(f'C_2,1,2 = {C_2_1_2}')
    print(f'C_2,2,2 = {C_2_2_2}')
    print(f'C_2,3,2 = {C_2_3_2}')
    print(f'C_2,4,2 = {C_2_4_2}')'''

    # This has been verified:
    '''print(f' C_1,2,1" = {np.array([[w*sin(gamma_1) + w*cot(gamma_1)**2/a],
                                   [0],
                                   [0]])}')'''

    print(f'C_2,1,1 = {T_1_2_new @ C_2_1_2}')
    print(f'C_2,2,1 = {T_1_2_new @ C_2_2_2}')
    print(f'C_2,3,1 = {T_1_2_new @ C_2_3_2}')
    print(f'C_2,4,1 = {T_1_2_new @ C_2_4_2}')

    '''print(f'C_2_1_1" = {L_2*y_2_1doubleprime}')
    print(np.linalg.norm(y_2_1doubleprime))'''

    '''print(f'C_0_1_1" = {C_0_1_1doubleprime}')
    print(f'C_0,1,1" = {T_1doubleprime_1 @ C_0_1_1}')
    print(f'C_0,2,1" = {T_1doubleprime_1 @ C_0_2_1}')
    print(f'C_0,3,1" = {T_1doubleprime_1 @ C_0_3_1}')
    print(f'C_0,4,1" = {T_1doubleprime_1 @ C_0_4_1}')'''

    # This portion of the code currently returns the wrong points. Except C_3_1_1 is right.
    print(f'C_3,1,1 = {T_1_2_new @ T_2_3 @ C_3_1_3}')
    print(f'C_3,2,1 = {T_1_2_new @ T_2_3 @ C_3_2_3}')
    print(f'C_3,3,1 = {T_1_2_new @ T_2_3 @ C_3_3_3}')
    print(f'C_3,4,1 = {T_1_2_new @ T_2_3 @ C_3_4_3}')

    '''print(f'C_3,1,3 = {C_3_1_3}')
    print(f'C_3,2,3 = {C_3_2_3}')
    print(f'C_3,3,3 = {C_3_3_3}')
    print(f'C_3,4,3 = {C_3_4_3}')'''

    print(T_1_2_new)

