# Calculating Elastic Constants of Cubic Fe Using Quantum ESPRESSO

This repository contains the necessary files and instructions to compute the elastic constants of cubic Fe using Quantum ESPRESSO.

## Files Overview

- **`0.txt`**  
  Contains the atomic coordinates of the unstrained system.

- **`qe_stress_values.txt`**  
  Provides the stress tensor values obtained from Quantum ESPRESSO. Each column represents stress tensor data for the following strain directions:
  - Positive: x, y, z, yz, xz, xy
  - Negative: x, y, z, yz, xz, xy

- **Strained Coordinate Files**  
  - `x_0.0025.in`, `y_0.0025.in`, ..., etc.:  
    These files include the atomic coordinates for the system strained along various directions with a strain magnitude of ±0.0025.

## Usage Instructions
1. **Run Calculations**  
   Perform stress calculations for each strained configuration using Quantum ESPRESSO.


