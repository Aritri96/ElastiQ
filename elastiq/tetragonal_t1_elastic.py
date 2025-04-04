import numpy as np

# File paths
stress_file = 'stress_tensors.dat'
strain_file = 'calculated_strain.dat'

# Load stress data (skip filename column)
S = np.genfromtxt(stress_file, skip_header=0, usecols=(1, 2, 3, 4, 5, 6))

# Load strain data (skip filename column)
E = np.genfromtxt(strain_file, skip_header=1, usecols=(1, 2, 3, 4, 5, 6))

# Ensure shape compatibility
if S.shape != E.shape:
    raise ValueError(f"Shape mismatch: stress {S.shape}, strain {E.shape}")

# Observed stress and applied strain
sobs = S
eapp = E

# ========== RIGHT-HAND SIDE VECTOR (C) ==========
C1 = np.dot(sobs[:, 0], eapp[:, 0]) + np.dot(sobs[:, 1], eapp[:, 1])
C2 = np.dot(sobs[:, 0], eapp[:, 1]) + np.dot(sobs[:, 1], eapp[:, 0])
C3 = np.dot(sobs[:, 0], eapp[:, 2]) + np.dot(sobs[:, 1], eapp[:, 2]) + np.dot(sobs[:, 2], eapp[:, 0] + eapp[:, 1])
C4 = np.dot(sobs[:, 2], eapp[:, 2])
C5 = np.dot(sobs[:, 3], eapp[:, 3]) + np.dot(sobs[:, 4], eapp[:, 4])
C6 = np.dot(sobs[:, 5], eapp[:, 5])
C = np.array([C1, C2, C3, C4, C5, C6])

# ========== MATRIX A ==========
A = np.zeros((6, 6))

A[0, 0] = np.dot(eapp[:, 0], eapp[:, 0]) + np.dot(eapp[:, 1], eapp[:, 1])
A[0, 1] = 2 * np.dot(eapp[:, 0], eapp[:, 1])
A[0, 2] = np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 2])
A[0, 3] = 0
A[0, 4] = 0
A[0, 5] = 0

A[1, 0] = A[0, 1]
A[1, 1] = A[0, 0]
A[1, 2] = A[0, 2]
A[1, 3] = 0
A[1, 4] = 0
A[1, 5] = 0

A[2, 0] = A[0, 2]
A[2, 1] = A[0, 2]
A[2, 2] = (
    np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 0] + eapp[:, 1]) +
    2 * np.dot(eapp[:, 2], eapp[:, 2])
)
A[2, 3] = A[0, 2]
A[2, 4] = 0
A[2, 5] = 0

A[3, 0] = 0
A[3, 1] = 0
A[3, 2] = A[0, 2]
A[3, 3] = np.dot(eapp[:, 2], eapp[:, 2])
A[3, 4] = 0
A[3, 5] = 0

A[4, 4] = np.dot(eapp[:, 3], eapp[:, 3]) + np.dot(eapp[:, 4], eapp[:, 4])
A[5, 5] = np.dot(eapp[:, 5], eapp[:, 5])

# Symmetry
A[4, 0] = A[4, 1] = A[4, 2] = A[4, 3] = A[4, 5] = 0
A[5, 0] = A[5, 1] = A[5, 2] = A[5, 3] = A[5, 4] = 0

# Solve for elastic constants
X = np.linalg.solve(A, C)
C11, C12, C13, C33, C44, C66 = X

# Output
print("\nInitial elastic constants (assuming stress in GPa):")
print(f"Iteration 0: C11 = {C11:.4f} GPa  C12 = {C12:.4f} GPa  C13 = {C13:.4f} GPa")
print(f"             C33 = {C33:.4f} GPa  C44 = {C44:.4f} GPa  C66 = {C66:.4f} GPa")
