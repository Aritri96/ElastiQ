import os
import glob

def rewrite_in_files_with_coordinates():
    # Get list of all .out files in the current directory
    out_files = glob.glob("*.out")

    if not out_files:
        raise FileNotFoundError("No .out files found in the current directory.")

    for out_filename in out_files:
        txt_filename = out_filename.replace('.out', '.txt')

        # Extract final coordinates from the .out file
        final_coords = extract_final_coordinates(out_filename)

        if not final_coords:
            print(f"Warning: No final coordinates found in file: {out_filename}. Skipping...")
            continue

        # Write the coordinates to a .txt file
        write_coords_to_txt(txt_filename, final_coords)
        print(f"Created coordinate file: {txt_filename}")

def extract_final_coordinates(out_filename):
    final_coords = []
    reading_coords = False

    with open(out_filename, 'r') as file:
        for line in file:
            line = line.strip()

            if 'Begin final coordinates' in line:
                reading_coords = True
                continue

            if 'End final coordinates' in line:
                reading_coords = False
                continue

            if reading_coords:
                tokens = line.split()
                if len(tokens) == 4:  # Format: Atom x y z
                    final_coords.append([float(tokens[1]), float(tokens[2]), float(tokens[3])])

    return final_coords

def write_coords_to_txt(txt_filename, final_coords):
    with open(txt_filename, 'w') as file:
        for coord in final_coords:
            file.write(f"{coord[0]:.12f} {coord[1]:.12f} {coord[2]:.12f}\n")

# Call the function when running as a script
if __name__ == "__main__":
    rewrite_in_files_with_coordinates()
