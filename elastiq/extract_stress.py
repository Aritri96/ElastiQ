import glob
import re

def extract_stress_tensors():
    files = glob.glob("*.out")
    if not files:
        raise FileNotFoundError("No .out files found in the current directory.")

    stress_filename = 'stress_tensors.dat'

    with open(stress_filename, 'w') as fout:
        for filename in files:
            print(f"Processing file: {filename}")
            with open(filename, 'r') as fin:
                lines = fin.readlines()

            stress_tensor = None
            found_section = False

            for i, line in enumerate(lines):
                if 'Computing stress (Cartesian axis) and pressure' in line:
                    for j in range(i+1, min(i+11, len(lines))):
                        if '(kbar)' in lines[j]:
                            if j+3 < len(lines):
                                try:
                                    s1 = list(map(float, lines[j+1].split()))
                                    s2 = list(map(float, lines[j+2].split()))
                                    s3 = list(map(float, lines[j+3].split()))

                                    if len(s1) >= 3 and len(s2) >= 3 and len(s3) >= 3:
                                        stress_tensor = [s1[-3:], s2[-3:], s3[-3:]]
                                        found_section = True
                                except ValueError:
                                    continue
                            break

            if found_section and stress_tensor:
                s11 = -0.1 * stress_tensor[0][0]
                s22 = -0.1 * stress_tensor[1][1]
                s33 = -0.1 * stress_tensor[2][2]
                s23 = -0.1 * stress_tensor[1][2]
                s13 = -0.1 * stress_tensor[0][2]
                s12 = -0.1 * stress_tensor[0][1]

                fout.write(f"{filename}\t{round(s11, 4):10.4f}\t{round(s22, 4):10.4f}\t"
                           f"{round(s33, 4):10.4f}\t{round(s23, 4):10.4f}\t"
                           f"{round(s13, 4):10.4f}\t{round(s12, 4):10.4f}\n")
            else:
                print(f"Warning: No stress tensor found in file: {filename}")

    print(f"All stress tensors written to: {stress_filename}")

# Run as script
if __name__ == "__main__":
    extract_stress_tensors()
