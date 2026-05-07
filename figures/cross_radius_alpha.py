"""Cross-radius variance scaling exponent α(r) for the Schelling FSS study.

α < -2.0 = trivial CLT averaging (sub-critical, L^-2).
α ≈ -2.0 = exact CLT, marginal.
α > -2.0 (less negative) = anomalous / possibly critical scaling.
"""
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
DEST = ROOT / "figures" / "cross_radius_alpha.png"

# Pull radius=1 and radius=2 from prior CI runs (Moore baseline + Chebyshev r=2)
d12 = np.load(ROOT / "outputs/ci_experiments/radius2-results/radius2_results.npz", allow_pickle=True)
records = [
    {"r": 1, "k": 8,  "F": 23,   "Tc": float(d12["Tc_R1"]), "alpha": float(d12["alpha_R1"]),
     "vars": list(d12["var_R1"]), "L_fss": list(d12["L_fss"])},
    {"r": 2, "k": 24, "F": 181,  "Tc": float(d12["Tc_R2"]), "alpha": float(d12["alpha_R2"]),
     "vars": list(d12["var_R2"]), "L_fss": list(d12["L_fss"])},
]

# Pull r >= 3 from multiradius runs as they appear
for r in (3, 4, 5, 6):
    p = ROOT / f"outputs/data/multiradius_R{r}.npz"
    if not p.exists():
        continue
    dr = np.load(p, allow_pickle=True)
    records.append({
        "r": r, "k": int(dr["k"]), "F": int(dr["F_k_size"]),
        "Tc": float(dr["T_c"]), "alpha": float(dr["alpha"]),
        "vars": list(dr["variances"]), "L_fss": list(dr["L_fss"]),
    })

records.sort(key=lambda x: x["r"])

# Compute apples-to-apples alphas using only common L_fss = [40, 80] across all radii.
# Some radii sampled L=20 too; drop it for fair comparison.
def alpha_on_L(rec, L_target=(40.0, 80.0)):
    L = np.array(rec["L_fss"], dtype=float)
    V = np.array(rec["vars"])
    mask = np.isin(L, L_target)
    if mask.sum() < 2:
        return rec["alpha"]
    return float(np.polyfit(np.log(L[mask]), np.log(V[mask]), 1)[0])

for rec in records:
    rec["alpha_L4080"] = alpha_on_L(rec)

# Plot α(r) with criticality threshold
fig, axes = plt.subplots(1, 2, figsize=(11, 4.0), dpi=200)

# Left: α(r), both full-grid and apples-to-apples [40,80] only
ax = axes[0]
rs = [rec["r"] for rec in records]
alphas = [rec["alpha"] for rec in records]
alphas_4080 = [rec["alpha_L4080"] for rec in records]
labels = [f"|F|={rec['F']}" for rec in records]
ax.axhline(-2.0, color="#888", linestyle=":", linewidth=1.0, label=r"trivial CLT $\alpha = -2$")
ax.axhline(0.0,  color="#aa5", linestyle=":", linewidth=1.0, label=r"critical boundary $\alpha = 0$")
ax.plot(rs, alphas,      "o-", color="#2E5077", linewidth=1.6, markersize=10, label="α (full L grid)")
ax.plot(rs, alphas_4080, "s--", color="#A56336", linewidth=1.2, markersize=8, label="α (L=40,80 only)")
for r, a, lab in zip(rs, alphas, labels):
    ax.text(r, a + 0.4, lab, ha="center", va="bottom", fontsize=9, color="#444")
ax.set_xlabel("Neighborhood radius r (Chebyshev)")
ax.set_ylabel(r"Variance scaling exponent $\alpha$")
ax.set_title(r"Cross-radius scaling exponent $\alpha(r)$", loc="left", pad=8, fontsize=10.5)
ax.set_xticks(rs)
ax.legend(loc="lower right", framealpha=0.95, fontsize=8.5)

# Right: log-log Var(L) per radius
ax = axes[1]
colors = ["#2E5077", "#A56336", "#4A8074", "#9B3A2D", "#6B4F8C", "#3B7B5E"]
for c, rec in zip(colors, records):
    L = np.array(rec["L_fss"], dtype=float)
    V = np.array(rec["vars"])
    ax.loglog(L, V, "o-", color=c, label=f"r={rec['r']}, α={rec['alpha']:+.2f}",
              linewidth=1.4, markersize=7)
ax.set_xlabel("Lattice size L")
ax.set_ylabel("Var(S) at $T_c(r)$")
ax.set_title(r"Per-radius variance scaling Var(S) vs L", loc="left", pad=8, fontsize=10.5)
ax.legend(loc="lower left", framealpha=0.95)

for ax in axes:
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(DEST, dpi=200, bbox_inches="tight")
print(f"Wrote {DEST}")
print(f"Records ({len(records)} radii):")
for rec in records:
    print(f"  r={rec['r']} k={rec['k']} |F|={rec['F']} T_c={rec['Tc']:.4f} alpha={rec['alpha']:+.4f}")
