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
# Calculate C vector
C = np.zeros(13)
C[0] = np.dot(sobs[:, 0], eapp[:, 0])
C[1] = np.dot(sobs[:, 0], eapp[:, 1]) + np.dot(sobs[:, 1], eapp[:, 0])
C[2] = np.dot(sobs[:, 0], eapp[:, 2]) + np.dot(sobs[:, 2], eapp[:, 0])
C[3] = np.dot(sobs[:, 0], eapp[:, 4]) + np.dot(sobs[:, 4], eapp[:, 0])
C[4] = np.dot(sobs[:, 1], eapp[:, 1])
C[5] = np.dot(sobs[:, 1], eapp[:, 2]) + np.dot(sobs[:, 2], eapp[:, 1])
C[6] = np.dot(sobs[:, 1], eapp[:, 4]) + np.dot(sobs[:, 4], eapp[:, 1])
C[7] = np.dot(sobs[:, 2], eapp[:, 2])
C[8] = np.dot(sobs[:, 2], eapp[:, 4]) + np.dot(sobs[:, 4], eapp[:, 2])
C[9] = np.dot(sobs[:, 3], eapp[:, 3])
C[10] = np.dot(sobs[:, 3], eapp[:, 5]) + np.dot(sobs[:, 5], eapp[:, 3])
C[11] = np.dot(sobs[:, 4], eapp[:, 4])
C[12] = np.dot(sobs[:, 5], eapp[:, 5])

# Calculate A matrix
A = np.zeros((13, 13))
for i in range(13):
    for j in range(13):
        if i < 6 and j < 6:
            A[i, j] = np.dot(eapp[:, i], eapp[:, j])
        else:
            A[i, j] = 0

# Solve for X (elastic constants)
try:
    A_inv = np.linalg.inv(A)
    X = np.dot(A_inv, C)
    print("Elastic Constants:")
    print(f"C11 = {X[0]:.6f}")
    print(f"C12 = {X[1]:.6f}")
    print(f"C13 = {X[2]:.6f}")
    print(f"C15 = {X[3]:.6f}")
    print(f"C22 = {X[4]:.6f}")
    print(f"C23 = {X[5]:.6f}")
    print(f"C25 = {X[6]:.6f}")
    print(f"C33 = {X[7]:.6f}")
    print(f"C35 = {X[8]:.6f}")
    print(f"C44 = {X[9]:.6f}")
    print(f"C46 = {X[10]:.6f}")
    print(f"C55 = {X[11]:.6f}")
    print(f"C66 = {X[12]:.6f}")
except np.linalg.LinAlgError as e:
    print(f"Error: Unable to invert A matrix. {e}")
