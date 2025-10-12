# EOM2025 - Entropy-Oriented Mechanics (EOM)

This repository contains the code, datasets, and documentation for the Entropy-Oriented Mechanics (EOM) framework, a unified control-theoretic approach for optimizing order fidelity and entropy production in far-from-equilibrium material systems. Developed by Truong Xuan Khanh and Truong Quynh Hoa at Clevix LLC, Hanoi, Vietnam, EOM is detailed in the paper "Entropy-Oriented Mechanics (EOM): Order–Energy Co-Optimization for Multi-State Material Systems" (Version 1.0-rc, December 2025).

## Overview
EOM integrates sequence-order fidelity (measured by the Order Compliance Index, OCI) and entropy production cost (σ(t)) into a single optimization objective:
- **J[u(t)] = α OCI - β σ - γ E[u(t)]**, where u(t) is a controllable input (e.g., current, voltage, light intensity, mechanical stress).
- Key indices: OCI, Entropic Compliance Index (ECI), Energy Dissipation Ratio (EDR), Energy–Order Ratio (EOR), and Stability-Dissipation Factor (SDF).
- Validated on the Oxford Battery Dataset (2017) and FigShare Memristor Datasets (2024), showing 23-35% reduction in cumulative entropy while maintaining OCI ≥ 0.9.

## Repository Structure
- `/code/`: Python scripts for optimization (PSO, RL) and data analysis.
- `/data/`: Links or samples of Oxford Battery and FigShare Memristor datasets.
- `/figures/`: Plots and figures (e.g., Pareto fronts, EOM indices).
- `/results/`: Raw data and computed metrics (e.g., OCI, EDR, SDF).
- `README.md`: This file.
- `LICENSE`: Open-source license (e.g., MIT or CC-BY).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ClevixLab/EOM2025.git
   cd EOM2025
