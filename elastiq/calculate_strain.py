import os
import numpy as np
import glob

# Constants
h = 4.0
fac = 1 / (np.pi * h**3)

# Use current directory
folder_path = os.getcwd()

# Ask user for reference configuration file
ref_filename = input("Enter the reference file (e.g., 0.txt): ").strip()
scf_path = os.path.join(folder_path, ref_filename)

# Check if reference file exists
if not os.path.isfile(scf_path):
    raise FileNotFoundError(f"{ref_filename} not found in {folder_path}")

# Load reference structure
scf = np.loadtxt(scf_path)

# Output file
output_file = os.path.join(folder_path, 'calculated_strain.dat')
with open(output_file, 'w') as fid:
    fid.write('Filename\tEps11\tEps22\tEps33\tEps23\tEps13\tEps12\n')

    # List all .txt files except the reference file
    files = glob.glob(os.path.join(folder_path, '*.txt'))
    files = [f for f in files if os.path.basename(f) != ref_filename]

    for file_path in files:
        file_name = os.path.basename(file_path)

        try:
            deform = np.loadtxt(file_path)
        except Exception:
            print(f"⚠️ Failed to load {file_name}. Skipping.")
            continue

        total = scf.shape[0]
        eqdij = np.zeros((total, total))
        dij = np.zeros((total, total))
        Bx = np.zeros((total, total))
        By = np.zeros((total, total))
        Bz = np.zeros((total, total))
        bx = np.zeros((total, total))
        by = np.zeros((total, total))
        bz = np.zeros((total, total))

        for i in range(total):
            for j in range(i, total):
                eqx, eqy, eqz = scf[j, :3] - scf[i, :3]
                dx, dy, dz = deform[j, :3] - deform[i, :3]

                eqdij[i, j] = eqdij[j, i] = np.linalg.norm([eqx, eqy, eqz])
                Bx[i, j] = Bx[j, i] = eqx
                By[i, j] = By[j, i] = eqy
                Bz[i, j] = Bz[j, i] = eqz

                dij[i, j] = dij[j, i] = np.linalg.norm([dx, dy, dz])
                bx[i, j] = bx[j, i] = dx
                by[i, j] = by[j, i] = dy
                bz[i, j] = bz[j, i] = dz

                if i == j:
                    eqdij[i, j] = dij[i, j] = 10000

        F = np.zeros((total, 9))
        epsmic = np.zeros((total, 9))
        success = True

        for i in range(total):
            D = np.zeros((3, 3))
            A = np.zeros((3, 3))

            min_eqdij_i = np.min(eqdij[:, i])
            for j in range(total):
                q = (eqdij[i, j] - min_eqdij_i) / h
                if q < 1:
                    w = fac * (1 - 1.5 * q**2 * (1 - q / 2))
                elif q < 2:
                    w = fac / 4 * (2 - q)**3
                else:
                    w = 0

                Bij = np.array([Bx[i, j], By[i, j], Bz[i, j]])
                bij = np.array([bx[i, j], by[i, j], bz[i, j]])

                D += w * np.outer(Bij, Bij)
                A += w * np.outer(bij, Bij)

            if np.linalg.cond(D) > 1e12:
                print(f"⚠️ D matrix nearly singular for {file_name} at atom {i+1}. Skipping file.")
                success = False
                break

            Fhat = A @ np.linalg.inv(D)
            F[i, :] = Fhat.T.flatten()
            epshat = 0.5 * (Fhat.T @ Fhat - np.eye(3))
            epsmic[i, :] = epshat.T.flatten()

        if success:
            avgepsmic = np.mean(epsmic, axis=0)
            avgepsmicmat = avgepsmic.reshape((3, 3)).T

            strain_f = [
                avgepsmicmat[0, 0],
                avgepsmicmat[1, 1],
                avgepsmicmat[2, 2],
                2 * avgepsmicmat[1, 2],
                2 * avgepsmicmat[0, 2],
                2 * avgepsmicmat[0, 1]
            ]

            fid.write(f"{file_name}\t" + "\t".join(f"{s:.12g}" for s in strain_f) + "\n")
            print(f"✅ Processed: {file_name}")

print(f"✅ Strain data written to {output_file}")
