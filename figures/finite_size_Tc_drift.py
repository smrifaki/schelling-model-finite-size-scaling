"""Finite-size T_c drift across L for r=4, r=5, r=6.

For a critical second-order transition, T_c(L) → T_c^∞ converges to a single
limit. For a smoothly-varying non-critical transition, T_c(L) drifts
monotonically with no convergence to a limit on accessible L.

We extract T_c per L by finding the T at which Binder U_4 crosses 0.5 (the
midpoint between the disordered plateau +2/3 and zero-ordering negative tail).
This is a model-free per-L T_c proxy that avoids the dS/dT estimator's L=40 bias."""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid", context="paper")
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.5,
    "axes.titlesize": 10.5,
    "axes.labelsize": 10.5,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9,
})

ROOT = Path("/Users/mrifaki/Projects/schelling-model-finite-size-scaling")
DEST = ROOT / "figures" / "finite_size_Tc_drift.png"


def find_Tc_at_threshold(T, U4, threshold=0.5):
    """Find T at which U_4 crosses threshold (going up)."""
    diff = U4 - threshold
    sign_changes = np.where(np.diff(np.sign(diff)))[0]
    if len(sign_changes) == 0:
        return None
    i = sign_changes[0]
    if (diff[i] - diff[i+1]) == 0:
        return None
    f = diff[i] / (diff[i] - diff[i+1])
    return float(T[i] + f * (T[i+1] - T[i]))


# Load 3-L Binder data for r=4, r=5, r=6
records = []
for r in (4, 5, 6):
    p = ROOT / f"outputs/data/binder_r{r}_L160.npz"
    d = np.load(p, allow_pickle=True)
    T = d["T"]
    L_LIST = list(d["L"])
    U4 = d["U4_per_L"]
    Tc_per_L = {}
    for i, L in enumerate(L_LIST):
        Tc = find_Tc_at_threshold(T, U4[i], threshold=0.5)
        if Tc is not None:
            Tc_per_L[int(L)] = Tc
    records.append({"r": r, "L_to_Tc": Tc_per_L})

# Plot: per-r, T_c(L) trajectory
fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=200)
colors = ["#2E5077", "#A56336", "#9B3A2D"]
markers = ["o", "s", "^"]

for rec, color, marker in zip(records, colors, markers):
    Ls = sorted(rec["L_to_Tc"].keys())
    Tcs = [rec["L_to_Tc"][L] for L in Ls]
    ax.plot(Ls, Tcs, marker + "-", color=color, linewidth=1.6, markersize=10,
            label=f"r={rec['r']} (k={ {4:80, 5:120, 6:168}[rec['r']]})")
    # Annotate per-L points
    for L, Tc in zip(Ls, Tcs):
        ax.annotate(f"L={L}\nT_c={Tc:.4f}",
                    xy=(L, Tc), xytext=(0, 12), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, color=color, alpha=0.8)

ax.set_xscale("log")
ax.set_xlabel("Lattice size L")
ax.set_ylabel(r"$T_c$ at $U_4 = 0.5$ crossing")
ax.set_title(r"Finite-size $T_c(L)$ drifts monotonically — no L-independent critical point",
             loc="left", pad=10, fontsize=10)
ax.set_xticks([40, 80, 160])
ax.set_xticklabels(["40", "80", "160"])
ax.legend(loc="lower left", framealpha=0.95)

for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(DEST, dpi=200, bbox_inches="tight")
print(f"Wrote {DEST}")
print("\nT_c(L) per radius:")
for rec in records:
    print(f"  r={rec['r']}: {rec['L_to_Tc']}")
