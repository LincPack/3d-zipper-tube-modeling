from zipper_tube import Tube
import numpy as np

tube = Tube(0.25, 0.25, 90, 90, 90)

# # Example 1: Vary theta, keep l and gamma constant
# l_vals = [2.0]
# theta_vals = np.linspace(30, 60, 3) # Test with 3 different theta values
# gamma_vals = [90]
# tube.analyze_joint_behavior(l_values=l_vals, theta_values=theta_vals, gamma_values=gamma_vals, alpha_steps=10)

# Example 2: Vary gamma, keep l and theta constant
# l_vals = [2.0]
# theta_vals = [45]
# gamma_vals = np.linspace(60, 120, 3) # Test with 3 different gamma values
# tube.analyze_joint_behavior(l_values=l_vals, theta_values=theta_vals, gamma_values=gamma_vals, alpha_steps=10)

# Example 3: Vary both theta and gamma (this will generate 2x2=4 paths)
# l_vals = [2.0]
# theta_vals = [30, 60]
# gamma_vals = [75, 105]
# tube.analyze_joint_behavior(l_values=l_vals, theta_values=theta_vals, gamma_values=gamma_vals, alpha_steps=10)


tube.add_joint(1.2505, 85.99, 54.30)
tube.add_joint(1.2505, 77.99, 154.96)
# tube.add_joint(1.2505, 101.87, 55.36)
# tube.add_joint(1.2505, 44.56, 152.20)
# tube.add_joint(1.2505, 114.63, 60.84)

# tube.add_joint(2, 45, 90)
# tube.add_joint(2, 45, 90)
tube.visualize(rep_method='t')
tube.print_points()
# tube.show_path()
