# ElastiQ
ElastiQ is a Python-based tool for calculating elastic constants of materials using stress and strained coordinate data obtained from DFT calculation

## Features
- Supports cubic and hexagonal material symmetries.
- Calculates elastic constants like C11, C12, C44, and more.
# Input Requirements
## Stress Data
Provide stress data in the following format
strain type=         strain_x	strain_y	strain_z	strain_yz	strain_xz	strain_xy	strain_neg_x	strain_neg_y	strain_neg_z	strain_neg_yz	strain_neg_xz	strain_neg_xy
stress component sxx=[6.86	   3.6	    3.6	    -0.03	      -0.03	    -0.03	    -7.16	        -3.7	        -3.7	          -0.03	       -0.03	        -0.03];
stress component syy=[3.61	   6.86	     3.6	   -0.03	    -0.03	    -0.03	    -3.69	         -7.16	       -3.7	          -0.03	        -0.03	        -0.03];
stress component szz=[3.61	   3.6	    6.86	    -0.03	    -0.04	    -0.03	     -3.69	        -3.7	        -7.16	        -0.03	        -0.03	        -0.03];
stress component syz=[0.00	    0	        0	        2.26	    0	        0	          0	            0	            0	            -2.26	        0	          0.00];
stress component sxz=[0.00	     0	      0	        0	        2.26	     0	        0	            0	            0	            0	          -2.26        	0.00];
stress component sxy=[0.00	      0	      0	        0	        0	      2.26	        0	            0	            0	            0	            0	          -2.26];

Notes:
Each row corresponds to the stress tensor components under a specific strain

## Strained Coordinates
The coordinates of the strained system must be provided in the same order as the stress values.
### Example:
If the first column of the stress data corresponds to strain_x, when the code prompts for strained system coordinates, you should provide the coordinates for the system strained along the x-direction first.
Similarly, ensure all subsequent coordinates are in the order of their corresponding stress data.

# Usage Example
## Prepare Input Files:
stress.txt: Contains stress tensor components obtained from DFT (see above format).
strain_x.txt, strain_y.txt, ...: Coordinates of the system under different strains.

# Installation Instructions
##Step 1: Clone the Repository
Open a terminal (or Command Prompt) and run:
git clone https://github.com/yourusername/ElastiQ.git

## Navigate to the project directory:
cd ElastiQ
Step 2: Install the Tool

1. Install the tool using pip in "editable" mode:
pip install -e .
2. If successful, you should see a message indicating that elastiq has been installed.

## Run ElastiQ:
1. Open a terminal and type:
elastiq

# Troubleshooting
If elastiq is not recognized as a command:

 ## 1. Ensure it is installed correctly using:
    pip show elastiq
 ## 2. If installed but not working, add the Scripts directory to your PATH:
C:\Users\<Your Username>\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts
