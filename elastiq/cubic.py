import numpy as np

# Load stress and strain data from files
filename1 = 'stress_for_c_final.dat'
filename2 = 'strain_for_c_final.dat'

# Load data, skipping the first column and reading only columns 1 to 6 (0-indexed)
S = np.loadtxt(filename1, usecols=range(1, 7))
E = np.loadtxt(filename2, usecols=range(1, 7))

# Check if the number of rows match in both files
if S.shape[0] != E.shape[0] or S.shape[1] != 6 or E.shape[1] != 6:
    print("Error: Files must have the same number of rows and 6 columns.")
    exit()

# Extract rows dynamically based on the number of strains
num_strains = S.shape[0]
sobs = S.copy()
eapp = E.copy()

#print("Stress observations (sobs):")
##print(sobs)

#print("Strain applications (eapp):")
#print(eapp)

# Calculate C
C = np.zeros(3)
C[0] = np.dot(sobs[:, 0], eapp[:, 0]) + np.dot(sobs[:, 1], eapp[:, 1]) + np.dot(sobs[:, 2], eapp[:, 2])
C[1] = (np.dot(sobs[:, 0], eapp[:, 1] + eapp[:, 2]) +
        np.dot(sobs[:, 1], eapp[:, 0] + eapp[:, 2]) +
        np.dot(sobs[:, 2], eapp[:, 0] + eapp[:, 1]))
C[2] = np.dot(sobs[:, 3], eapp[:, 3]) + np.dot(sobs[:, 4], eapp[:, 4]) + np.dot(sobs[:, 5], eapp[:, 5])

#print("C values:")
#print(C)

# Calculate A
A = np.zeros((3, 3))
A[0, 0] = (np.dot(eapp[:, 0], eapp[:, 0]) + np.dot(eapp[:, 1], eapp[:, 1]) +
           np.dot(eapp[:, 2], eapp[:, 2]))
A[0, 1] = 2 * (np.dot(eapp[:, 0], eapp[:, 1]) +
               np.dot(eapp[:, 0], eapp[:, 2]) +
               np.dot(eapp[:, 1], eapp[:, 2]))
A[0, 2] = 0

A[1, 0] = (np.dot(eapp[:, 0], eapp[:, 1] + eapp[:, 2]) +
           np.dot(eapp[:, 1], eapp[:, 0] + eapp[:, 2]) +
           np.dot(eapp[:, 2], eapp[:, 0] + eapp[:, 1]))
A[1, 1] = ((np.dot(eapp[:, 0] + eapp[:, 1], eapp[:, 0] + eapp[:, 1])) +
           (np.dot(eapp[:, 0] + eapp[:, 2], eapp[:, 0] + eapp[:, 2])) +
           (np.dot(eapp[:, 1] + eapp[:, 2], eapp[:, 1] + eapp[:, 2])))
A[1, 2] = 0

A[2, 0] = 0
A[2, 1] = 0
A[2, 2] = (np.dot(eapp[:, 3], eapp[:, 3]) + np.dot(eapp[:, 4], eapp[:, 4]) +
           np.dot(eapp[:, 5], eapp[:, 5]))

#print("Matrix A:")
#print(A)

# Invert A and solve for X
try:
    A_inv = np.linalg.inv(A)
except np.linalg.LinAlgError as e:
    print(f"Error: Matrix A is singular and cannot be inverted: {e}")
    exit()

#print("Inverse of A:")
#print(A_inv)

X = np.dot(A_inv, C)

# Extract and print elastic constants
C11 = X[0]  # X[0] corresponds to C11
C12 = X[1]  # X[1] corresponds to C12
C44 = X[2]  # X[2] corresponds to C44

print("Elastic constants:")
print(f"C11 = {C11:.6f} (in GPa or appropriate units)")
print(f"C12 = {C12:.6f} (in GPa or appropriate units)")
print(f"C44 = {C44:.6f} (in GPa or appropriate units)")
