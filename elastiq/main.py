import os
import subprocess

def main():
    print("*********Welcome to ElastiQ*********")
    # Prompt user for material symmetry
    symmetry = input("Enter the symmetry of the material (cubic/hexagonal): ").strip().lower()

    if symmetry not in ['cubic', 'hexagonal']:
        print("Error: Invalid symmetry. Please enter 'cubic' or 'hexagonal'.")
        return

    # Run the stress_strain.py script
    print("Running stress_strain.py...")
    subprocess.run(["python", "stress_strain.py"])

    # Run the appropriate script based on symmetry
    if symmetry == "cubic":
        print("Running cubic.py for cubic symmetry...")
        subprocess.run(["python", "cubic.py"])
    elif symmetry == "hexagonal":
        print("Running hexagonal.py for hexagonal symmetry...")
        subprocess.run(["python", "hexagonal.py"])

if __name__ == "__main__":
    main()
