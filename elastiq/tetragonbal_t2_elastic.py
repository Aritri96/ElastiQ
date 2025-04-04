import numpy as np

# Filenames
filename1 = 'stress_tensors.txt'
filename2 = 'strain_from_pkp.txt'

# Load stress and strain data (skip first column if it's filenames)
stressdat = np.genfromtxt(stress_file, skip_header=0, usecols=(1, 2, 3, 4, 5, 6))
straindat = np.genfromtxt(strain_file, skip_header=1, usecols=(1, 2, 3, 4, 5, 6))

# Use only first 4 rows for initial fit
sobs = stressdat[:4, :]
eapp = straindat[:4, :]

# Build strain matrix for least squares
strmat = []
for i in range(4):
    eps = eapp[i, :]
    row1 = [eps[0], eps[1], eps[2], eps[5], 0, 0, 0]
    row2 = [eps[1], eps[0], eps[2], -eps[5], 0, 0, 0]
    row3 = [0, 0, eps[0] + eps[1], 0, eps[2], 0, 0]
    row4 = [0, 0, 0, 0, 0, eps[3], 0]
    row5 = [0, 0, 0, 0, 0, eps[4], 0]
    row6 = [0, 0, 0, eps[0] - eps[1], 0, 0, eps[5]]
    strmat.extend([row1, row2, row3, row4, row5, row6])

strmat = np.array(strmat)  # Shape: (24, 7)
stress = sobs.T.flatten()  # Flattened 4x6 matrix into 24x1 vector

# Solve using least squares
X, _, _, _ = np.linalg.lstsq(strmat, stress, rcond=None)
C11, C12, C13, C16, C33, C44, C66 = X

# Print results
print(f"Iteration 0: C11 = {C11:.4f} GPa  C12 = {C12:.4f} GPa  C13 = {C13:.4f} GPa")
print(f"             C16 = {C16:.4f} GPa  C33 = {C33:.4f} GPa  C44 = {C44:.4f} GPa  C66 = {C66:.4f} GPa")
