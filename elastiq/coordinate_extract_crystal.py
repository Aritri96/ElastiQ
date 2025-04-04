import os
import glob
import numpy as np
import re

def crys_to_ang_convert():
    out_files = glob.glob("*.out")
    if not out_files:
        raise FileNotFoundError("No .out files found in the current directory.")

    for out_filename in out_files:
        base_name = os.path.splitext(out_filename)[0]
        in_filename = base_name + ".in"
        out_txt_filename = base_name + ".txt"

        if not os.path.isfile(in_filename):
            print(f"Warning: Corresponding .in file not found for {out_filename}. Skipping...")
            continue

        final_crystal_coords = extract_final_crystal_coordinates(out_filename)
        if final_crystal_coords is None:
            print(f"Warning: No final coordinates found in {out_filename}. Skipping...")
            continue

        cell_matrix = extract_cell_parameters(in_filename)
        if cell_matrix is None:
            print(f"Warning: CELL_PARAMETERS not found in {in_filename}. Skipping...")
            continue

        # Convert to Cartesian (angstroms)
        angstrom_coords = np.dot(final_crystal_coords, cell_matrix)

        # Write to .txt file
        with open(out_txt_filename, 'w') as f:
            for coord in angstrom_coords:
                f.write(f"{coord[0]:.12f} {coord[1]:.12f} {coord[2]:.12f}\n")

        print(f"Written final coordinates (in angstrom) to {out_txt_filename}")

def extract_final_crystal_coordinates(filename):
    final_coords = []
    reading = False

    with open(filename, 'r') as file:
        for line in file:
            line_lower = line.strip().lower()
            if 'begin final coordinates' in line_lower:
                reading = True
                continue
            elif 'end final coordinates' in line_lower:
                break
            elif reading:
                tokens = line.strip().split()
                if len(tokens) >= 4:
                    try:
                        coords = list(map(float, tokens[1:4]))
                        final_coords.append(coords)
                    except ValueError:
                        continue

    if final_coords:
        return np.array(final_coords)
    else:
        return None

def extract_cell_parameters(filename):
    with open(filename, 'r') as file:
        content = file.read()

    match = re.search(r"CELL_PARAMETERS.*?\n(.*?)\n(.*?)\n(.*?)\n", content, re.DOTALL)
    if not match:
        return None

    try:
        lines = match.groups()
        cell_matrix = np.array([list(map(float, line.split())) for line in lines])
        return cell_matrix
    except Exception:
        return None

# Run the script
if __name__ == "__main__":
    crys_to_ang_convert()
