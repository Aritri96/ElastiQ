import os
import subprocess

def run_script(script_name, args=None):
    """Utility to run a Python script with optional arguments."""
    try:
        command = ["python", script_name]
        if args:
            command.extend(args)
        subprocess.run(command, check=True)
        print(f"{script_name} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error: Script {e.cmd} failed with exit code {e.returncode}.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while running {script_name}: {e}")
        exit(1)

def main():
    print("********* Welcome to ElastiQ *********")

    # Step 1: Material symmetry
    symmetry = input("Enter the symmetry of the material (Cubic/Hexagonal/Trigonal/Tetragonal_T1/Tetragonal_T2/Orthorhombic/Monoclinic/Triclinic): ").strip().lower()
    valid_symmetries = ['cubic', 'hexagonal', 'trigonal', 'tetragonal_t1', 'tetragonal_t2', 'orthorhombic', 'monoclinic', 'triclinic']
    if symmetry not in valid_symmetries:
        print(f"Error: Invalid symmetry. Please enter one of {', '.join(valid_symmetries)}.")
        return

    # Step 2: Check input/output formats
    confirm_formats = input("Are your Quantum ESPRESSO input/output files in '.in' and '.out' formats? (yes/no): ").strip().lower()
    if confirm_formats != 'yes':
        print("Please ensure your input and output files are in '.in' and '.out' format before proceeding.")
        return

    # Step 3: Coordinate format
    coord_format = input("Are your atomic coordinates in 'angstrom' or 'crystal' format? ").strip().lower()
    if coord_format == "angstrom":
        run_script("coordinate_extract_angstrom.py")
    elif coord_format == "crystal":
        run_script("coordinate_extract_crystal.py")
    else:
        print("Error: Invalid coordinate format. Please enter 'angstrom' or 'crystal'.")
        return

    # Step 4: Extract stress
    run_script("extract_stress.py")

    # Step 5: Calculate strain (reference state will be asked inside the script)
    run_script("calculate_strain.py")

    # Step 6: Calculate elastic constants
    symmetry_script_map = {
        "cubic": "cubic_elastic.py",
        "hexagonal": "hexagonal_elastic.py",
        "trigonal": "trigonal_elastic.py",
        "tetragonal_t1": "tetragonal_t1_elastic.py",
        "tetragonal_t2": "tetragonal_t2_elastic.py",
        "orthorhombic": "orthorhombic_elastic.py",
        "monoclinic": "monoclinic_elastic.py",
        "triclinic": "triclinic_elastic.py"
    }

    elastic_script = symmetry_script_map[symmetry]
    run_script(elastic_script)

if __name__ == "__main__":
    main()
