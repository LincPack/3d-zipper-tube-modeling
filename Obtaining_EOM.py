import sympy as sp
from control.tube_class import Tube
from control.symbolic_export import export_symbolic_expression_to_pdf
import textwrap

tube = Tube()
tube.add_joint()
tube.add_joint()
tube.add_joint()
tube.add_joint()
tube.add_joint()
tube.add_joint()

gammas = [sp.pi/4, -sp.pi/4, sp.pi/4, sp.pi/4, -sp.pi/4, sp.pi/4]
thetas = [sp.pi/4, -sp.pi/4, 1.5, sp.pi/4, -sp.pi/4, 1.5]
lengths = [1, 5, 1, 5, 5, 10]

# print(len(tube.boxes))

# export_symbolic_expression_to_pdf(tube.boxes, filename='boxes5.pdf', output_dir='control')

# print(tube.get_EOM())
# tube.get_panel_energies()
# print(tube.energies)
# export_symbolic_expression_to_pdf(tube.get_EOM(gamma_values = gammas, theta_values = thetas, length_values = lengths), filename='EOM_2_Tubes.pdf', output_dir='control')
# # 1. Convert your data to a string first
output_data = str(tube.get_EOM(gamma_values=gammas, theta_values=thetas, length_values=lengths))

# 2. Wrap the text at 60 characters
wrapped_data = textwrap.fill(output_data, width=60)

# 3. Write it to the file
with open('control/EOM6_Tube.txt', 'w') as f:
    f.write(wrapped_data)

# print(tube.get_EOM(gamma_values = gammas, theta_values = thetas, length_values = lengths))
