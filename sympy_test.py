#%%
import sympy as sp

a, b, c, d = sp.symbols('a b c d')

A = sp.Matrix([a, b])
B = sp.Matrix([[c],[d]])

sp.pprint(A@B)

# %%
