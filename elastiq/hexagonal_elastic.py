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

# ========== INITIAL ELASTIC CONSTANT CALCULATION ==========

# Right-hand side vector C
C1 = np.dot(sobs[:, 0], eapp[:, 0]) + np.dot(sobs[:, 1], eapp[:, 1]) + 0.5 * np.dot(sobs[:, 5], eapp[:, 5])
C2 = np.dot(sobs[:, 0], eapp[:, 1]) + np.dot(sobs[:, 1], eapp[:, 0]) - 0.5 * np.dot(sobs[:, 5], eapp[:, 5])
C3 = np.dot(sobs[:, 0] + sobs[:, 1], eapp[:, 2]) + np.dot(sobs[:, 2], eapp[:, 0] + eapp[:, 1])
C4 = np.dot(sobs[:, 2], eapp[:, 2])
C5 = np.dot(sobs[:, 3], eapp[:, 3]) + np.dot(sobs[:, 4], eapp[:, 4])
C = np.array([C1, C2, C3, C4, C5])

# Matrix A
A = np.zeros((5, 5))
A[0, 0] = np.dot(eapp[:, 0], eapp[:, 0]) + np.dot(eapp[:, 1], eapp[:, 1]) + 0.25 * np.dot(eapp[:, 5], eapp[:, 5])
A[0, 1] = 2 * np.dot(eapp[:, 0], eapp[:, 1])
A[0, 2] = np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 2])
A[0, 3] = 0
A[0, 4] = 0

A[1, 0] = 2 * np.dot(eapp[:, 0], eapp[:, 1]) - 0.25 * np.dot(eapp[:, 5], eapp[:, 5])
A[1, 1] = A[0, 0]
A[1, 2] = A[0, 2]
A[1, 3] = 0
A[1, 4] = 0

A[2, 0] = A[0, 2]
A[2, 1] = A[0, 2]
A[2, 2] = 2 * np.dot(eapp[:, 2], eapp[:, 2]) + np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 0] + eapp[:, 1])
A[2, 3] = A[0, 2]
A[2, 4] = 0

A[3, 0] = 0
A[3, 1] = 0
A[3, 2] = A[0, 2]
A[3, 3] = np.dot(eapp[:, 2], eapp[:, 2])
A[3, 4] = 0

A[4, 4] = np.dot(eapp[:, 3], eapp[:, 3]) + np.dot(eapp[:, 4], eapp[:, 4])

# Solve the system
X = np.linalg.solve(A, C)
C11, C12, C13, C33, C44 = X

# Display results
print("\nInitial elastic constants (assuming stress in GPa):")
print(f"C11 = {C11:.4f} GPa")
print(f"C12 = {C12:.4f} GPa")
print(f"C13 = {C13:.4f} GPa")
print(f"C33 = {C33:.4f} GPa")
print(f"C44 = {C44:.4f} GPa")