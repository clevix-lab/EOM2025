
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data" / "battery" / "oxford_sample.csv"
RES  = BASE / "results"
RES.mkdir(exist_ok=True, parents=True)

df = pd.read_csv(DATA)
t = df["time_s"].values
I = df["current_A"].values
V = df["voltage_V"].values
T = df["temp_C"].values + 273.15

# --- Phase segmentation (Oxford-friendly): explicit windows per cycle ---
# s1=CC (|I|>0.9A), s2=CV (0.2<|I|<=0.9A), s3=Rest (<=0.2A)
absI = np.abs(I)
s1 = absI > 0.9
s2 = (absI <= 0.9) & (absI > 0.2)
s3 = absI <= 0.2
state = np.zeros_like(I, dtype=int)
state[s1] = 1; state[s2] = 2; state[s3] = 3

# OCI by first-occurrence order per cycle
OCI_list = []
cycles = df["cycle"].unique()
for c in cycles:
    m = df["cycle"]==c
    idx = np.where(m)[0]
    st = state[idx]
    t_idx = idx
    def first_pos(k):
        w = np.where(st==k)[0]
        return t_idx[w[0]] if len(w) else None
    i1,i2,i3 = first_pos(1), first_pos(2), first_pos(3)
    if None in (i1,i2,i3):
        continue
    viol12 = 1.0 if i2<i1 else 0.0
    viol23 = 1.0 if i3<i2 else 0.0
    OCI_list.append(1.0 - 0.5*(viol12+viol23))

OCI = float(np.mean(OCI_list)) if len(OCI_list)>0 else 0.0

# Sigma proxy with rolling V_eq
V_eq = pd.Series(V).rolling(600, min_periods=1).min().values
eta = V - V_eq
sigma = (I*eta)/T
Pin = np.abs(I*V)

SigInt = np.trapz(np.abs(sigma), t)
sigma_star = np.median(sigma)
sigma_max  = max(np.max(np.abs(sigma)), 1e-9)
ECI = 1.0 - (1.0/len(t))*np.sum(np.abs(sigma - sigma_star)/sigma_max)
EDR = np.trapz(np.abs(sigma), t) / np.trapz(Pin, t)
EOR = OCI / max(SigInt, 1e-9)
SDF = 1.0 / np.var(sigma)
idx_base = dict(OCI=OCI, ECI=ECI, EDR=EDR, EOR=EOR, SDF=SDF, SigInt=SigInt)

# --- SOM and EOM transforms (simple heuristics) ---
def smooth(x, w=201):
    k = np.ones(w)/w
    return np.convolve(x, k, mode='same')

def som_current(I):
    # keep CC (phase 1) longer, mid reduced
    J = I.copy()
    J[(np.abs(J)<=0.9) & (np.abs(J)>0.2)] *= 0.85
    return smooth(J, 201)

def eom_current(I):
    J = I.copy()
    # stronger reduction where |I| is largest, slight on mid, minimal on rest
    J[np.abs(J)>0.9] *= 0.7
    J[(np.abs(J)<=0.9) & (np.abs(J)>0.2)] *= 0.9
    J[np.abs(J)<=0.2] *= 0.98
    return smooth(J, 201)

def compute_indices(I_variant, label):
    absI = np.abs(I_variant)
    s1 = absI > 0.9; s2 = (absI<=0.9)&(absI>0.2); s3 = absI<=0.2
    # cycle-level OCI
    OCI_list = []
    for c in cycles:
        m = df["cycle"]==c; idx = np.where(m)[0]; st = np.zeros_like(I_variant, dtype=int)
        st[s1]=1; st[s2]=2; st[s3]=3; st = st[idx]
        def first_pos(k):
            w = np.where(st==k)[0]
            return idx[w[0]] if len(w) else None
        i1,i2,i3 = first_pos(1), first_pos(2), first_pos(3)
        if None in (i1,i2,i3): continue
        viol12 = 1.0 if i2<i1 else 0.0
        viol23 = 1.0 if i3<i2 else 0.0
        OCI_list.append(1.0 - 0.5*(viol12+viol23))
    OCI = float(np.mean(OCI_list)) if len(OCI_list)>0 else 0.0
    V_eq = pd.Series(V).rolling(600, min_periods=1).min().values
    eta = V - V_eq
    sigma = (I_variant*eta)/T
    SigInt = np.trapz(np.abs(sigma), t)
    sigma_star = np.median(sigma); sigma_max = max(np.max(np.abs(sigma)), 1e-9)
    ECI = 1.0 - (1.0/len(t))*np.sum(np.abs(sigma - sigma_star)/sigma_max)
    Pin = np.abs(I_variant*V)
    EDR = np.trapz(np.abs(sigma), t) / np.trapz(Pin, t)
    EOR = OCI / max(SigInt, 1e-9)
    SDF = 1.0 / np.var(sigma)
    return dict(label=label, OCI=OCI, ECI=ECI, EDR=EDR, EOR=EOR, SDF=SDF, SigInt=SigInt)

I_som = som_current(I);  I_eom = eom_current(I)
idx_som = compute_indices(I_som, "SOM")
idx_eom = compute_indices(I_eom, "EOM")

# Save summary and plots
import pandas as pd, matplotlib.pyplot as plt
summary = pd.DataFrame([
    {"regime":"Baseline", **{k:v for k,v in idx_base.items() if k!='SigInt'}},
    {"regime":"SOM", **{k:v for k,v in idx_som.items() if k!='SigInt'}},
    {"regime":"EOM", **{k:v for k,v in idx_eom.items() if k!='SigInt'}},
])
summary.to_csv(RES/"oxford_eom_indices_summary.csv", index=False)

plt.figure()
plt.scatter([idx_base["SigInt"], idx_som["SigInt"], idx_eom["SigInt"]],
            [idx_base["OCI"],   idx_som["OCI"],   idx_eom["OCI"]], s=90, marker='s')
for lab, idx in [("Baseline",idx_base),("SOM",idx_som),("EOM",idx_eom)]:
    plt.text(idx["SigInt"], idx["OCI"]+0.005, lab, ha="center")
plt.xlabel("Integral of |sigma|  (∫|σ| dt)"); plt.ylabel("OCI")
plt.title("Oxford Sample: Pareto (Baseline–SOM–EOM)")
plt.grid(True, linestyle="--", linewidth=0.5)
plt.tight_layout(); plt.savefig(RES/"oxford_pareto.png", dpi=160)
print("Saved:", RES/"oxford_eom_indices_summary.csv", "and", RES/"oxford_pareto.png")
