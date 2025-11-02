# EOM-AI: Entropic Exponents Reveal Universal Degradation Attractors in Lithium-Ion Batteries

[<image-card alt="DOI" src="https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg" ></image-card>](https://doi.org/10.5281/zenodo.XXXXXXX)  
[<image-card alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" ></image-card>](https://opensource.org/licenses/MIT)  
[<image-card alt="Python 3.9+" src="https://img.shields.io/badge/python-3.9+-blue.svg" ></image-card>](https://www.python.org/downloads/)  
[<image-card alt="Nature Energy" src="https://img.shields.io/badge/Nature%20Energy-under%20review-red" ></image-card>](https://www.nature.com/nenergy/)

---

## **Abstract**

Battery degradation remains a critical barrier to electric vehicle adoption, costing over $10 billion annually in lost capacity. Here we introduce **Entropy-Oriented Mechanics (EOM)**, a thermodynamic-control framework that defines the **entropic Lyapunov exponent** $\lambda_\text{EOM} = \dot{\Sigma}/\Sigma$ as a universal degradation metric.  

Using **7,000+ real-world drive cycles from NASA and Oxford datasets**, we reveal a **global stability attractor** at $(\lambda_\text{EOM}, \kappa_\text{EOM}, \Sigma_\text{EOM}) = (0, 0, 0)$ in healthy cells. In degraded operation, $\lambda_\text{EOM}$ scales with **internal resistance** ($r = 0.71$, $p < 10^{-200}$) and **power loss** ($r = 0.28$), forming an **entropy–impedance bridge** and **energy–entropy balance law**.  

A **3D Pareto manifold** defines the **Entropy Efficiency Zone**, enabling **AI-driven control** that **reduces entropy production by 23–35%** and **extends lifetime by 25%**. **EOM-AI outperforms phenomenological models**, offering a **physics-informed path to next-generation battery management**.

---

## **Authors & Correspondence**

**Truong Xuan Khanh¹,²,***, **Truong Quynh Hoa¹**, **Co-Author²**  

¹ H/&K Research Lab, Clevix LLC, Hanoi, Vietnam  
² H/&K Research Lab, Clevix LLC, Hanoi, Vietnam  

*Correspondence: khanh@clevix.vn

---

## **Key Results**

| Metric | EOM-AI | Severson (2019) | Ma et al. (2024) |
|--------|--------|------------------|------------------|
| **SOH RMSE (%)** | **1.8** | 3.2 | 2.9 |
| **RUL Error (cycles)** | **42** | 85 | 68 |
| **Entropy-aware?** | Yes | No | Partial |
| **Cross-chemistry?** | Yes (NMC + LFP) | No | No |

> **25% lifetime extension** | **Entropy–Impedance Bridge**: $r = 0.71$, $p < 10^{-200}$

---

## **Quick Start**

```bash
git clone https://github.com/clevix-lab/EOM-AI-Battery-Degradation.git
cd EOM-AI-Battery-Degradation
conda env create -f environment.yml
conda activate eom-ai
python scripts/EOM_AI_Extended.py --all
