import numpy as np

# Load stress and strain data from files
filename1 = 'stress_for_c_final.dat'
filename2 = 'strain_for_c_final.dat'

# Load data, skipping the first column (if necessary) and reading only the relevant columns
S = np.loadtxt(filename1, usecols=range(1, 7))
E = np.loadtxt(filename2, usecols=range(1, 7))

# Verify the number of rows and columns
if S.shape[0] != E.shape[0] or S.shape[1] != 6 or E.shape[1] != 6:
    print("Error: Files must have the same number of rows and 6 columns.")
    exit()

# Number of strains
N = S.shape[0]

# Extract stress and strain observations
sobs = S.copy()
eapp = E.copy()

#print("Stress observations (sobs):")
#print(sobs)

#print("Strain applications (eapp):")
##print(eapp)

# Calculate C matrix
C = np.zeros(5)
C[0] = (np.dot(sobs[:, 0], eapp[:, 0]) +
        np.dot(sobs[:, 1], eapp[:, 1]) +
        0.5 * np.dot(sobs[:, 5], eapp[:, 5]))
C[1] = (np.dot(sobs[:, 0], eapp[:, 1]) +
        np.dot(sobs[:, 1], eapp[:, 0]) -
        0.5 * np.dot(sobs[:, 5], eapp[:, 5]))
C[2] = (np.dot(sobs[:, 0] + sobs[:, 1], eapp[:, 2]) +
        np.dot(sobs[:, 2], eapp[:, 0] + eapp[:, 1]))
C[3] = np.dot(sobs[:, 2], eapp[:, 2])
C[4] = (np.dot(sobs[:, 3], eapp[:, 3]) +
        np.dot(sobs[:, 4], eapp[:, 4]))

#print("C values:")
#print(C)

# Calculate A matrix
A = np.zeros((5, 5))
A[0, 0] = (np.dot(eapp[:, 0], eapp[:, 0]) +
           np.dot(eapp[:, 1], eapp[:, 1]) +
           0.25 * np.dot(eapp[:, 5], eapp[:, 5]))
A[0, 1] = 2 * np.dot(eapp[:, 0], eapp[:, 1])
A[0, 2] = np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 2])
A[0, 3] = 0
A[0, 4] = 0

A[1, 0] = 2 * np.dot(eapp[:, 0], eapp[:, 1]) - 0.25 * np.dot(eapp[:, 5], eapp[:, 5])
A[1, 1] = (np.dot(eapp[:, 0], eapp[:, 0]) +
           np.dot(eapp[:, 1], eapp[:, 1]) +
           0.25 * np.dot(eapp[:, 5], eapp[:, 5]))
A[1, 2] = np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 2])
A[1, 3] = 0
A[1, 4] = 0

A[2, 0] = np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 2])
A[2, 1] = np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 2])
A[2, 2] = (2 * np.dot(eapp[:, 2], eapp[:, 2]) +
           np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 0] + eapp[:, 1]))
A[2, 3] = np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 2])
A[2, 4] = 0

A[3, 0] = 0
A[3, 1] = 0
A[3, 2] = np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 2])
A[3, 3] = np.dot(eapp[:, 2], eapp[:, 2])
A[3, 4] = 0

A[4, 0] = 0
A[4, 1] = 0
A[4, 2] = 0
A[4, 3] = 0
A[4, 4] = (np.dot(eapp[:, 3], eapp[:, 3]) +
           np.dot(eapp[:, 4], eapp[:, 4]))

#print("Matrix A:")
#print(A)

# Invert A and solve for X
try:
    A_inv = np.linalg.inv(A)
except np.linalg.LinAlgError as e:
    print(f"Error: Matrix A is singular and cannot be inverted: {e}")
    exit()

X = np.dot(A_inv, C)

# Extract and print elastic constants
C11 = X[0]
C12 = X[1]
C13 = X[2]
C33 = X[3]
C44 = X[4]

print("Elastic constants:")
print(f"C11 = {C11:.6f}")
print(f"C12 = {C12:.6f}")
print(f"C13 = {C13:.6f}")
print(f"C33 = {C33:.6f}")
print(f"C44 = {C44:.6f}")
