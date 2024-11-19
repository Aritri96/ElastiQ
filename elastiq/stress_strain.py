import numpy as np

# Prompt for the file containing the initial coordinates
initial_file = input("Enter the name of the file containing initial 0-strain structure: ")

# Load initial coordinates
initial = np.loadtxt(initial_file)

# Ask user for the stress components file
stress_file_name = input("Enter the name of the file containing stress components: ")

# Function to parse stress components from the file
def parse_stress_file(file_name):
    stress_data = {}
    with open(file_name, 'r') as file:
        for line in file:
            if '=' in line:
                key, values = line.split('=')
                key = key.strip()
                values = list(map(float, values.strip('[];\n').split()))
                stress_data[key] = values
    return stress_data

# Parse the stress components
stress_components = parse_stress_file(stress_file_name)
sxx = stress_components.get("sxx", [])
syy = stress_components.get("syy", [])
szz = stress_components.get("szz", [])
syz = stress_components.get("syz", [])
sxz = stress_components.get("sxz", [])
sxy = stress_components.get("sxy", [])

# Check if all components have been read
if not all([sxx, syy, szz, syz, sxz, sxy]):
    raise ValueError("Some stress components are missing in the input file.")

# Ask user for the number of strains applied
num_strains = int(input("Enter the number of strains applied: "))

# Ask for the filenames containing strained system coordinates
strain_files = []
for i in range(num_strains):
    strain_file = input(f"Enter the filename for strain system {i + 1}: ")
    strain_files.append(strain_file)

# File suffixes for output (for labeling purposes)
file_suffixes = [f"strain_{i + 1}" for i in range(num_strains)]

# Open output files
strain_output_file = open('strain_for_c_final.dat', 'a')
strain_stress_output_file = open('strain_for_stress_final.dat', 'a')
stress_output_file = open('stress_for_c_final.dat', 'a')

for i, strain_file in enumerate(strain_files):
    # Load displacement data
    try:
        final_data = np.loadtxt(strain_file)
    except FileNotFoundError:
        print(f"File {strain_file} not found. Skipping.")
        continue
    
    # Calculate displacements
    displacement = final_data - initial
    xdisp, ydisp, zdisp = displacement[:, 0], displacement[:, 1], displacement[:, 2]
    xinit, yinit, zinit = initial[:, 0], initial[:, 1], initial[:, 2]
    const = np.ones_like(xinit)
    
    # Perform regression
    initdata = np.column_stack([xinit, yinit, zinit, const])
    ux, _, _, _ = np.linalg.lstsq(initdata, xdisp, rcond=None)
    uy, _, _, _ = np.linalg.lstsq(initdata, ydisp, rcond=None)
    uz, _, _, _ = np.linalg.lstsq(initdata, zdisp, rcond=None)
    
    initxydata = np.column_stack([xinit, yinit, const])
    inityzdata = np.column_stack([yinit, zinit, const])
    initxzdata = np.column_stack([xinit, zinit, const])
    
    yfxz, _, _, _ = np.linalg.lstsq(initxzdata, yinit, rcond=None)
    zfxy, _, _, _ = np.linalg.lstsq(initxydata, zinit, rcond=None)
    xfyz, _, _, _ = np.linalg.lstsq(inityzdata, xinit, rcond=None)
    
    # Compute deformation gradient
    def_grad = np.array([
        [ux[0] + ux[1] * yfxz[0] + ux[2] * zfxy[0], ux[0] * xfyz[0] + ux[1] + ux[2] * zfxy[1], ux[0] * xfyz[1] + ux[1] * yfxz[1] + ux[2]],
        [uy[0] + uy[1] * yfxz[0] + uy[2] * zfxy[0], uy[0] * xfyz[0] + uy[1] + uy[2] * zfxy[1], uy[0] * xfyz[1] + uy[1] * yfxz[1] + uy[2]],
        [uz[0] + uz[1] * yfxz[0] + uz[2] * zfxy[0], uz[0] * xfyz[0] + uz[1] + uz[2] * zfxy[1], uz[0] * xfyz[1] + uz[1] * yfxz[1] + uz[2]]
    ])
    def_grad1 = def_grad + np.eye(3)
    
    # Calculate strain tensor
    strain_full = 0.5 * (np.dot(def_grad1.T, def_grad1) - np.eye(3))
    strain = [strain_full[0, 0], strain_full[1, 1], strain_full[2, 2], 
              2 * strain_full[1, 2], 2 * strain_full[0, 2], 2 * strain_full[0, 1]]
    
    # Write strain data
    strain_output_file.write(f"{file_suffixes[i]}\t" + "\t".join(map(str, strain)) + "\n")
    
    # Calculate components for stress-strain relationship
    uxx, uxy, uxz = def_grad[0, 0], def_grad[0, 1], def_grad[0, 2]
    uyx, uyy, uyz = def_grad[1, 0], def_grad[1, 1], def_grad[1, 2]
    uzx, uzy, uzz = def_grad[2, 0], def_grad[2, 1], def_grad[2, 2]
    S1 = [uxx, uyy, uzz, uyz + uzy, uxz + uzx, uxy + uyx]
    strain_stress_output_file.write(f"{file_suffixes[i]}\t" + "\t".join(map(str, S1)) + "\n")
    
    # Define stress tensor
    s = np.array([
        [0.1 * sxx[i], 0.1 * sxy[i], 0.1 * sxz[i]],
        [0.1 * sxy[i], 0.1 * syy[i], 0.1 * syz[i]],
        [0.1 * sxz[i], 0.1 * syz[i], 0.1 * szz[i]]
    ])
    detF = np.linalg.det(def_grad1)
    Finv = np.linalg.inv(def_grad1)
    FinvT = Finv.T
    t = detF * np.dot(Finv, np.dot(s, FinvT))
    
    Es = [t[0, 0], t[1, 1], t[2, 2], t[1, 2], t[0, 2], t[0, 1]]
    stress_output_file.write(f"{file_suffixes[i]}\t" + "\t".join(map(str, Es)) + "\n")

# Close files
strain_output_file.close()
strain_stress_output_file.close()
stress_output_file.close()
