"""Binder cumulant U_4(T) curves at radius=4 across L. Crossings give T_c independently."""
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
DEST = ROOT / "figures" / "binder_r4_crossing.png"

d = np.load(ROOT / "outputs/data/binder_r4.npz", allow_pickle=True)
T = d["T"]
L_LIST = list(d["L"])
U4 = d["U4_per_L"]
crossings = d["T_crossings"]

fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=200)
colors = ["#2E5077", "#A56336", "#4A8074", "#9B3A2D"]
for L, u, c in zip(L_LIST, U4, colors):
    ax.plot(T, u, "o-", color=c, label=f"L={L}", linewidth=1.6, markersize=6)

# Annotate crossings
for c in crossings:
    ax.axvline(c, color="#aa3", linestyle="--", linewidth=1.0, alpha=0.7)
    ax.text(c, ax.get_ylim()[0] + 0.05, f"T_c (Binder) = {c:.4f}",
            rotation=90, ha="right", va="bottom", fontsize=8.5, color="#aa3")

# Reference: dS/dT-derived T_c
ax.axvline(0.347, color="#888", linestyle=":", linewidth=1.0)
ax.text(0.347, ax.get_ylim()[1] - 0.02, " dS/dT T_c = 0.347",
        rotation=90, ha="left", va="top", fontsize=8.5, color="#666")

ax.set_xlabel("Tolerance T")
ax.set_ylabel(r"Binder cumulant $U_4 = 1 - \langle S^4\rangle / 3\langle S^2\rangle^2$")
ax.set_title(r"Binder cumulant crossings at r=4 confirm $T_c$ independently",
             loc="left", pad=10, fontsize=10.5)
ax.legend(loc="lower right", framealpha=0.95)

for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(DEST, dpi=200, bbox_inches="tight")
print(f"Wrote {DEST}")
