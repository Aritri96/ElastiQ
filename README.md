# ElastiQ: Automated Elastic Constant Calculator from Quantum ESPRESSO Outputs

Welcome to **ElastiQ**, a Python-based framework for automating the workflow of computing **single crystal elastic constants** using input and output files from **Quantum ESPRESSO**. It supports all 7 crystal systems and seamlessly processes relaxed coordinates, stress tensors, and strain tensors to yield the elastic constants for your material system.

---

## 🔧 Features

- Supports: Cubic, Hexagonal, Trigonal, Tetragonal (T1 & T2), Orthorhombic, Monoclinic, and Triclinic symmetries.
- Handles both `angstrom` and `crystal` coordinate formats.
- Automatically extracts stress from `.out` files.
- Computes strain tensors from relaxed configurations.
- Modular architecture: each step is a separate script, making debugging and customization easy.

---


---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ElastiQ.git
cd ElastiQ
2. Requirements
Python 3.x

Modules: os, subprocess, sys

⚠️ No third-party packages are required unless your individual scripts depend on them.

3. Prepare Your Files
Place your Quantum ESPRESSO .in and .out files in the current directory.

Ensure the filenames for input and output match appropriately.

Make sure relaxed configurations are available for each strained case.

4. Run the Tool
bash
Copy
Edit
python main.py
You will be prompted to:

Select the material symmetry.

Confirm if your input/output files are correctly formatted.

Choose between angstrom or crystal coordinate format.

The script will automatically process and guide you through each step.

********* Welcome to ElastiQ *********
Enter the symmetry of the material (Cubic/Hexagonal/Trigonal/...): cubic
Are your Quantum ESPRESSO input/output files in '.in' and '.out' formats? (yes/no): yes
Are your atomic coordinates in 'angstrom' or 'crystal' format? angstrom
Running coordinate_extract_angstrom.py...
Running extract_stress.py...
Running calculate_strain.py...
Running cubic_elastic.py...


🤝 Contributing
Contributions are welcome! If you'd like to improve this tool:

Fork the repository 🍴

Create a new feature branch (git checkout -b feature/your-feature)

Commit your changes (git commit -am 'Add some feature')

Push to the branch (git push origin feature/your-feature)

Open a pull request 🚀

If you encounter any issues or have suggestions, feel free to open an issue on GitHub or contact the maintainer directly.

