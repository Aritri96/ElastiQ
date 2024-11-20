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

# Compute the C vector
C = np.zeros(21)
C[0] = np.dot(sobs[:, 0], eapp[:, 0])
C[1] = np.dot(sobs[:, 0], eapp[:, 1]) + np.dot(sobs[:, 1], eapp[:, 0])
C[2] = np.dot(sobs[:, 0], eapp[:, 2]) + np.dot(sobs[:, 2], eapp[:, 0])
C[3] = np.dot(sobs[:, 0], eapp[:, 3]) + np.dot(sobs[:, 3], eapp[:, 0])
C[4] = np.dot(sobs[:, 0], eapp[:, 4]) + np.dot(sobs[:, 4], eapp[:, 0])
C[5] = np.dot(sobs[:, 0], eapp[:, 5]) + np.dot(sobs[:, 5], eapp[:, 0])
C[6] = np.dot(sobs[:, 1], eapp[:, 1])
C[7] = np.dot(sobs[:, 1], eapp[:, 2]) + np.dot(sobs[:, 2], eapp[:, 1])
C[8] = np.dot(sobs[:, 1], eapp[:, 3]) + np.dot(sobs[:, 3], eapp[:, 1])
C[9] = np.dot(sobs[:, 1], eapp[:, 4]) + np.dot(sobs[:, 4], eapp[:, 1])
C[10] = np.dot(sobs[:, 1], eapp[:, 5]) + np.dot(sobs[:, 5], eapp[:, 1])
C[11] = np.dot(sobs[:, 2], eapp[:, 2])
C[12] = np.dot(sobs[:, 2], eapp[:, 3]) + np.dot(sobs[:, 3], eapp[:, 2])
C[13] = np.dot(sobs[:, 2], eapp[:, 4]) + np.dot(sobs[:, 4], eapp[:, 2])
C[14] = np.dot(sobs[:, 2], eapp[:, 5]) + np.dot(sobs[:, 5], eapp[:, 2])
C[15] = np.dot(sobs[:, 3], eapp[:, 3])
C[16] = np.dot(sobs[:, 3], eapp[:, 4]) + np.dot(sobs[:, 4], eapp[:, 3])
C[17] = np.dot(sobs[:, 3], eapp[:, 5]) + np.dot(sobs[:, 5], eapp[:, 3])
C[18] = np.dot(sobs[:, 4], eapp[:, 4])
C[19] = np.dot(sobs[:, 4], eapp[:, 5]) + np.dot(sobs[:, 5], eapp[:, 4])
C[20] = np.dot(sobs[:, 5], eapp[:, 5])

# Initialize the A matrix
A = np.zeros((21, 21))
for i in range(6):
    for j in range(6):
        A[i, j] = np.dot(eapp[:, i], eapp[:, j])

# Add the remaining entries to A based on the MATLAB logic
for i in range(6, 21):
    for j in range(6, 21):
        A[i, j] = np.dot(eapp[:, i % 6], eapp[:, j % 6])

# Solve for X (elastic constants)
try:
    A_inv = np.linalg.inv(A)
    X = np.dot(A_inv, C)
    print("Elastic Constants:")
    for i in range(21):
        print(f"C{i + 1} = {X[i]:.6f}")
except np.linalg.LinAlgError as e:
    print(f"Error: Unable to invert A matrix. {e}")

# Output size of C
print(f"Size of C vector: {C.shape}")
