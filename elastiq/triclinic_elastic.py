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


# Manually compute C vector elements
C1 = np.dot(sobs[:, 0], eapp[:, 0])
C2 = np.dot(sobs[:, 0], eapp[:, 1]) + np.dot(sobs[:, 1], eapp[:, 0])
C3 = np.dot(sobs[:, 0], eapp[:, 2]) + np.dot(sobs[:, 2], eapp[:, 0])
C4 = np.dot(sobs[:, 0], eapp[:, 3]) + np.dot(sobs[:, 3], eapp[:, 0])
C5 = np.dot(sobs[:, 0], eapp[:, 4]) + np.dot(sobs[:, 4], eapp[:, 0])
C6 = np.dot(sobs[:, 0], eapp[:, 5]) + np.dot(sobs[:, 5], eapp[:, 0])
C7 = np.dot(sobs[:, 1], eapp[:, 1])
C8 = np.dot(sobs[:, 1], eapp[:, 2]) + np.dot(sobs[:, 2], eapp[:, 1])
C9 = np.dot(sobs[:, 1], eapp[:, 3]) + np.dot(sobs[:, 3], eapp[:, 1])
C10 = np.dot(sobs[:, 1], eapp[:, 4]) + np.dot(sobs[:, 4], eapp[:, 1])
C11 = np.dot(sobs[:, 1], eapp[:, 5]) + np.dot(sobs[:, 5], eapp[:, 1])
C12 = np.dot(sobs[:, 2], eapp[:, 2])
C13 = np.dot(sobs[:, 2], eapp[:, 3]) + np.dot(sobs[:, 3], eapp[:, 2])
C14 = np.dot(sobs[:, 2], eapp[:, 4]) + np.dot(sobs[:, 4], eapp[:, 2])
C15 = np.dot(sobs[:, 2], eapp[:, 5]) + np.dot(sobs[:, 5], eapp[:, 2])
C16 = np.dot(sobs[:, 3], eapp[:, 3])
C17 = np.dot(sobs[:, 3], eapp[:, 4]) + np.dot(sobs[:, 4], eapp[:, 3])
C18 = np.dot(sobs[:, 3], eapp[:, 5]) + np.dot(sobs[:, 5], eapp[:, 3])
C19 = np.dot(sobs[:, 4], eapp[:, 4])
C20 = np.dot(sobs[:, 4], eapp[:, 5]) + np.dot(sobs[:, 5], eapp[:, 4])
C21 = np.dot(sobs[:, 5], eapp[:, 5])
C = np.array([C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19, C20, C21])

# Define A matrix manually, row by row
A = np.zeros((21, 21))

# Row 1
A[0, 0] = np.dot(eapp[:, 0], eapp[:, 0])
A[0, 1] = np.dot(eapp[:, 1], eapp[:, 0])
A[0, 2] = np.dot(eapp[:, 2], eapp[:, 0])
A[0, 3] = np.dot(eapp[:, 3], eapp[:, 0])
A[0, 4] = np.dot(eapp[:, 4], eapp[:, 0])
A[0, 5] = np.dot(eapp[:, 5], eapp[:, 0])
# All others are zero and remain as initialized



# Row 2
A[1, 0] = np.dot(eapp[:, 0], eapp[:, 1])
A[1, 1] = np.dot(eapp[:, 1], eapp[:, 1]) + np.dot(eapp[:, 0], eapp[:, 0])
A[1, 2] = np.dot(eapp[:, 2], eapp[:, 1])
A[1, 3] = np.dot(eapp[:, 3], eapp[:, 1])
A[1, 4] = np.dot(eapp[:, 4], eapp[:, 1])
A[1, 5] = np.dot(eapp[:, 5], eapp[:, 1])
A[1, 6] = np.dot(eapp[:, 0], eapp[:, 1])
A[1, 7] = np.dot(eapp[:, 0], eapp[:, 2])
A[1, 8] = np.dot(eapp[:, 0], eapp[:, 3])
A[1, 9] = np.dot(eapp[:, 0], eapp[:, 4])
A[1,10] = np.dot(eapp[:, 0], eapp[:, 5])

# Row 3
A[2, 0] = np.dot(eapp[:, 0], eapp[:, 2])
A[2, 1] = np.dot(eapp[:, 1], eapp[:, 2])
A[2, 2] = np.dot(eapp[:, 2], eapp[:, 2]) + np.dot(eapp[:, 0], eapp[:, 0])
A[2, 3] = np.dot(eapp[:, 3], eapp[:, 2])
A[2, 4] = np.dot(eapp[:, 4], eapp[:, 2])
A[2, 5] = np.dot(eapp[:, 5], eapp[:, 2])
A[2, 7] = np.dot(eapp[:, 1], eapp[:, 0])
A[2,12] = np.dot(eapp[:, 0], eapp[:, 2])
A[2,13] = np.dot(eapp[:, 0], eapp[:, 3])
A[2,14] = np.dot(eapp[:, 0], eapp[:, 4])
A[2,15] = np.dot(eapp[:, 0], eapp[:, 5])

# Row 4
A[3, 0] = np.dot(eapp[:, 0], eapp[:, 3])
A[3, 1] = np.dot(eapp[:, 1], eapp[:, 3])
A[3, 2] = np.dot(eapp[:, 2], eapp[:, 3])
A[3, 3] = np.dot(eapp[:, 3], eapp[:, 3]) + np.dot(eapp[:, 0], eapp[:, 0])
A[3, 4] = np.dot(eapp[:, 4], eapp[:, 3])
A[3, 5] = np.dot(eapp[:, 5], eapp[:, 3])
A[3, 8] = np.dot(eapp[:, 1], eapp[:, 0])
A[3,13] = np.dot(eapp[:, 2], eapp[:, 0])
A[3,15] = np.dot(eapp[:, 3], eapp[:, 0])
A[3,16] = np.dot(eapp[:, 4], eapp[:, 0])
A[3,17] = np.dot(eapp[:, 5], eapp[:, 0])

# Continue manual construction of A matrix

# Row 5
A[4, 0] = np.dot(eapp[:, 0], eapp[:, 4])
A[4, 1] = np.dot(eapp[:, 1], eapp[:, 4])
A[4, 2] = np.dot(eapp[:, 2], eapp[:, 4])
A[4, 3] = np.dot(eapp[:, 3], eapp[:, 4])
A[4, 4] = np.dot(eapp[:, 4], eapp[:, 4]) + np.dot(eapp[:, 0], eapp[:, 0])
A[4, 5] = np.dot(eapp[:, 5], eapp[:, 4])
A[4,10] = np.dot(eapp[:, 1], eapp[:, 0])
A[4,13] = np.dot(eapp[:, 2], eapp[:, 0])
A[4,16] = np.dot(eapp[:, 3], eapp[:, 0])
A[4,18] = np.dot(eapp[:, 4], eapp[:, 0])
A[4,19] = np.dot(eapp[:, 5], eapp[:, 0])

# Row 6
A[5, 0] = np.dot(eapp[:, 0], eapp[:, 5])
A[5, 1] = np.dot(eapp[:, 1], eapp[:, 5])
A[5, 2] = np.dot(eapp[:, 2], eapp[:, 5])
A[5, 3] = np.dot(eapp[:, 3], eapp[:, 5])
A[5, 4] = np.dot(eapp[:, 4], eapp[:, 5])
A[5, 5] = np.dot(eapp[:, 5], eapp[:, 5]) + np.dot(eapp[:, 0], eapp[:, 0])
A[5,10] = np.dot(eapp[:, 1], eapp[:, 0])
A[5,14] = np.dot(eapp[:, 2], eapp[:, 0])
A[5,16] = np.dot(eapp[:, 3], eapp[:, 0])
A[5,19] = np.dot(eapp[:, 4], eapp[:, 0])
A[5,20] = np.dot(eapp[:, 5], eapp[:, 0])

# Row 7
A[6, 1] = np.dot(eapp[:, 0], eapp[:, 1])
A[6, 6] = np.dot(eapp[:, 1], eapp[:, 1])
A[6, 7] = np.dot(eapp[:, 2], eapp[:, 1])
A[6, 8] = np.dot(eapp[:, 3], eapp[:, 1])
A[6, 9] = np.dot(eapp[:, 4], eapp[:, 1])
A[6,10] = np.dot(eapp[:, 5], eapp[:, 1])

# Row 8
A[7, 1] = np.dot(eapp[:, 0], eapp[:, 2])
A[7, 2] = np.dot(eapp[:, 1], eapp[:, 2])
A[7, 7] = np.dot(eapp[:, 2], eapp[:, 2]) + np.dot(eapp[:, 1], eapp[:, 1])
A[7, 8] = np.dot(eapp[:, 3], eapp[:, 2])
A[7, 9] = np.dot(eapp[:, 4], eapp[:, 2])
A[7,10] = np.dot(eapp[:, 5], eapp[:, 2])
A[7,12] = np.dot(eapp[:, 2], eapp[:, 1])
A[7,13] = np.dot(eapp[:, 3], eapp[:, 1])
A[7,14] = np.dot(eapp[:, 4], eapp[:, 1])
A[7,15] = np.dot(eapp[:, 5], eapp[:, 1])

# Continue manual A matrix construction

# Row 9
A[8, 1] = np.dot(eapp[:, 0], eapp[:, 3])
A[8, 3] = np.dot(eapp[:, 1], eapp[:, 3])
A[8, 7] = np.dot(eapp[:, 2], eapp[:, 3])
A[8, 8] = np.dot(eapp[:, 3], eapp[:, 3]) + np.dot(eapp[:, 1], eapp[:, 1])
A[8, 9] = np.dot(eapp[:, 4], eapp[:, 3])
A[8,10] = np.dot(eapp[:, 5], eapp[:, 3])
A[8,13] = np.dot(eapp[:, 2], eapp[:, 1])
A[8,15] = np.dot(eapp[:, 3], eapp[:, 1])
A[8,16] = np.dot(eapp[:, 4], eapp[:, 1])
A[8,17] = np.dot(eapp[:, 5], eapp[:, 1])

# Row 10
A[9, 1] = np.dot(eapp[:, 0], eapp[:, 4])
A[9, 4] = np.dot(eapp[:, 1], eapp[:, 4])
A[9, 7] = np.dot(eapp[:, 2], eapp[:, 4])
A[9, 8] = np.dot(eapp[:, 3], eapp[:, 4])
A[9, 9] = np.dot(eapp[:, 4], eapp[:, 4]) + np.dot(eapp[:, 1], eapp[:, 1])
A[9,10] = np.dot(eapp[:, 5], eapp[:, 4])
A[9,13] = np.dot(eapp[:, 2], eapp[:, 3])
A[9,16] = np.dot(eapp[:, 3], eapp[:, 2])
A[9,17] = np.dot(eapp[:, 4], eapp[:, 2])
A[9,18] = np.dot(eapp[:, 5], eapp[:, 2])

# Row 11
A[10, 1] = np.dot(eapp[:, 0], eapp[:, 5])
A[10, 4] = np.dot(eapp[:, 1], eapp[:, 5])
A[10, 6] = np.dot(eapp[:, 2], eapp[:, 5])
A[10, 7] = np.dot(eapp[:, 3], eapp[:, 5])
A[10, 8] = np.dot(eapp[:, 4], eapp[:, 5])
A[10, 9] = np.dot(eapp[:, 5], eapp[:, 5]) + np.dot(eapp[:, 1], eapp[:, 1])
A[10,13] = np.dot(eapp[:, 2], eapp[:, 3])
A[10,16] = np.dot(eapp[:, 3], eapp[:, 2])
A[10,17] = np.dot(eapp[:, 4], eapp[:, 2])
A[10,18] = np.dot(eapp[:, 5], eapp[:, 2])

# Continue final rows

# Row 12
A[11, 2] = np.dot(eapp[:, 0], eapp[:, 5])
A[11, 7] = np.dot(eapp[:, 2], eapp[:, 1])
A[11, 8] = np.dot(eapp[:, 3], eapp[:, 1])
A[11, 9] = np.dot(eapp[:, 4], eapp[:, 1])
A[11,10] = np.dot(eapp[:, 5], eapp[:, 1])
A[11,11] = np.dot(eapp[:, 2], eapp[:, 2])
A[11,12] = np.dot(eapp[:, 2], eapp[:, 3])
A[11,13] = np.dot(eapp[:, 2], eapp[:, 4])
A[11,14] = np.dot(eapp[:, 2], eapp[:, 5])

# Row 13
A[12, 2] = np.dot(eapp[:, 0], eapp[:, 3])
A[12, 3] = np.dot(eapp[:, 0], eapp[:, 2])
A[12, 7] = np.dot(eapp[:, 2], eapp[:, 4])
A[12, 8] = np.dot(eapp[:, 2], eapp[:, 3])
A[12,12] = np.dot(eapp[:, 3], eapp[:, 3]) + np.dot(eapp[:, 2], eapp[:, 2])
A[12,13] = np.dot(eapp[:, 4], eapp[:, 3])
A[12,14] = np.dot(eapp[:, 5], eapp[:, 3])
A[12,15] = np.dot(eapp[:, 3], eapp[:, 2])
A[12,16] = np.dot(eapp[:, 4], eapp[:, 2])
A[12,17] = np.dot(eapp[:, 5], eapp[:, 2])

# Row 14
A[13, 2] = np.dot(eapp[:, 0], eapp[:, 4])
A[13, 4] = np.dot(eapp[:, 0], eapp[:, 2])
A[13, 7] = np.dot(eapp[:, 2], eapp[:, 5])
A[13, 9] = np.dot(eapp[:, 2], eapp[:, 3])
A[13,12] = np.dot(eapp[:, 3], eapp[:, 4])
A[13,13] = np.dot(eapp[:, 4], eapp[:, 4]) + np.dot(eapp[:, 3], eapp[:, 3])
A[13,14] = np.dot(eapp[:, 5], eapp[:, 4])
A[13,15] = np.dot(eapp[:, 3], eapp[:, 4])
A[13,16] = np.dot(eapp[:, 4], eapp[:, 3])
A[13,17] = np.dot(eapp[:, 5], eapp[:, 3])

# Fix and complete the final rows without using invalid index 6

# Row 15 (corrected)
A[14, 2] = np.dot(eapp[:, 0], eapp[:, 5])
A[14, 5] = np.dot(eapp[:, 0], eapp[:, 2])
A[14,12] = np.dot(eapp[:, 2], eapp[:, 5])
A[14,13] = np.dot(eapp[:, 3], eapp[:, 5])
A[14,14] = np.dot(eapp[:, 5], eapp[:, 5]) + np.dot(eapp[:, 2], eapp[:, 2])
A[14,15] = np.dot(eapp[:, 3], eapp[:, 5])
A[14,17] = np.dot(eapp[:, 3], eapp[:, 2])
A[14,19] = np.dot(eapp[:, 4], eapp[:, 2])
A[14,20] = np.dot(eapp[:, 5], eapp[:, 2])

# Row 16
A[15, 3] = np.dot(eapp[:, 0], eapp[:, 3])
A[15, 9] = np.dot(eapp[:, 1], eapp[:, 3])
A[15,12] = np.dot(eapp[:, 2], eapp[:, 3])
A[15,15] = np.dot(eapp[:, 3], eapp[:, 3])
A[15,16] = np.dot(eapp[:, 4], eapp[:, 3])
A[15,17] = np.dot(eapp[:, 5], eapp[:, 3])

# Row 17
A[16, 3] = np.dot(eapp[:, 0], eapp[:, 4])
A[16, 4] = np.dot(eapp[:, 0], eapp[:, 3])
A[16, 9] = np.dot(eapp[:, 1], eapp[:, 4])
A[16,10] = np.dot(eapp[:, 1], eapp[:, 3])
A[16,12] = np.dot(eapp[:, 2], eapp[:, 4])
A[16,13] = np.dot(eapp[:, 2], eapp[:, 3])
A[16,16] = np.dot(eapp[:, 4], eapp[:, 3])
A[16,17] = np.dot(eapp[:, 5], eapp[:, 3])
A[16,18] = np.dot(eapp[:, 4], eapp[:, 4])

# Row 18
A[17, 3] = np.dot(eapp[:, 0], eapp[:, 5])
A[17, 5] = np.dot(eapp[:, 0], eapp[:, 4])
A[17, 9] = np.dot(eapp[:, 1], eapp[:, 5])
A[17,11] = np.dot(eapp[:, 1], eapp[:, 4])
A[17,12] = np.dot(eapp[:, 2], eapp[:, 5])
A[17,14] = np.dot(eapp[:, 2], eapp[:, 4])
A[17,16] = np.dot(eapp[:, 4], eapp[:, 5])
A[17,17] = np.dot(eapp[:, 5], eapp[:, 5])
A[17,18] = np.dot(eapp[:, 4], eapp[:, 4])

# Row 19
A[18, 4] = np.dot(eapp[:, 0], eapp[:, 5])
A[18,10] = np.dot(eapp[:, 1], eapp[:, 5])
A[18,13] = np.dot(eapp[:, 2], eapp[:, 5])
A[18,16] = np.dot(eapp[:, 4], eapp[:, 5])
A[18,18] = np.dot(eapp[:, 5], eapp[:, 5])

# Row 20
A[19, 5] = np.dot(eapp[:, 0], eapp[:, 5])
A[19,10] = np.dot(eapp[:, 1], eapp[:, 5])
A[19,14] = np.dot(eapp[:, 2], eapp[:, 5])
A[19,17] = np.dot(eapp[:, 4], eapp[:, 5])
A[19,18] = np.dot(eapp[:, 5], eapp[:, 4])
A[19,19] = np.dot(eapp[:, 5], eapp[:, 5])

# Row 21
A[20, 5] = np.dot(eapp[:, 0], eapp[:, 5])
A[20,10] = np.dot(eapp[:, 1], eapp[:, 5])
A[20,14] = np.dot(eapp[:, 2], eapp[:, 5])
A[20,17] = np.dot(eapp[:, 4], eapp[:, 5])
A[20,19] = np.dot(eapp[:, 5], eapp[:, 4])
A[20,20] = np.dot(eapp[:, 5], eapp[:, 5])

# Symmetrize A
A = A + A.T - np.diag(A.diagonal())

# Solve system
X = np.linalg.solve(A, C)
labels = [
    'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
    'C22', 'C23', 'C24', 'C25', 'C26',
    'C33', 'C34', 'C35', 'C36',
    'C44', 'C45', 'C46',
    'C55', 'C56',
    'C66'
]
elastic_constants = dict(zip(labels, X))

print(f"C11 = {elastic_constants['C11']:.4f}  C12 = {elastic_constants['C12']:.4f}  C13 = {elastic_constants['C13']:.4f}  C14 = {elastic_constants['C14']:.4f}  C15 = {elastic_constants['C15']:.4f}  C16 = {elastic_constants['C16']:.4f}")
print(f"C22 = {elastic_constants['C22']:.4f}  C23 = {elastic_constants['C23']:.4f}  C24 = {elastic_constants['C24']:.4f}  C25 = {elastic_constants['C25']:.4f}  C26 = {elastic_constants['C26']:.4f}")
print(f"C33 = {elastic_constants['C33']:.4f}  C34 = {elastic_constants['C34']:.4f}  C35 = {elastic_constants['C35']:.4f}  C36 = {elastic_constants['C36']:.4f}")
print(f"C44 = {elastic_constants['C44']:.4f}  C45 = {elastic_constants['C45']:.4f}  C46 = {elastic_constants['C46']:.4f}")
print(f"C55 = {elastic_constants['C55']:.4f}  C56 = {elastic_constants['C56']:.4f}")
print(f"C66 = {elastic_constants['C66']:.4f}")







