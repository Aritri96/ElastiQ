import os
import subprocess

def main():
    print("*********Welcome to ElastiQ*********")

    # Prompt user for material symmetry
    symmetry = input("Enter the symmetry of the material (Cubic/Hexagonal/Trigonal/Tetragonal_T1/Tetragonal_T2/Orthorhombic/Monoclinic/Triclinic): ").strip().lower()

    # Validate symmetry input
    valid_symmetries = ['cubic', 'hexagonal', 'trigonal', 'tetragonal_t1', 'tetragonal_t2', 'orthorhombic', 'monoclinic', 'triclinic']
    if symmetry not in valid_symmetries:
        print(f"Error: Invalid symmetry. Please enter one of {', '.join([s.capitalize() for s in valid_symmetries])}.")
        return

    # Script mapping
    script_map = {
        "cubic": "cubic.py",
        "hexagonal": "hexagonal.py",
        "trigonal": "trigonal.py",
        "tetragonal_t1": "tetragonal_t1.py",
        "tetragonal_t2": "tetragonal_t2.py",
        "orthorhombic": "orthorhombic.py",
        "monoclinic": "monoclinic.py",
        "triclinic": "triclinic.py"
    }

    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stress_strain_path = os.path.join(script_dir, "stress_strain.py")
    symmetry_script_path = os.path.join(script_dir, script_map[symmetry])

    # Check if stress_strain.py exists
    if not os.path.exists(stress_strain_path):
        print("Error: stress_strain.py not found in the script directory.")
        return

    try:
        # Run the stress_strain.py script
        print("Running stress_strain.py...")
        subprocess.run(["python", stress_strain_path], check=True)
        print("stress_strain.py completed successfully.\n")

        # Check if symmetry-specific script exists
        if not os.path.exists(symmetry_script_path):
            print(f"Error: {script_map[symmetry]} not found in the script directory.")
            return

        # Run the appropriate script based on symmetry
        print(f"Running {script_map[symmetry]} for {symmetry.capitalize()} symmetry...")
        subprocess.run(["python", symmetry_script_path], check=True)
        print(f"{script_map[symmetry]} completed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error: Script {e.cmd} failed with exit code {e.returncode}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
