"""Extend r=4 FSS with L=160 to tighten α and Binder analysis."""
import sys, os, time, numpy as np
from joblib import Parallel, delayed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from benchmarking.multiradius_experiment import (
    chebyshev_offsets, run_model, RHO, F_A, segregation_index
)

RADIUS = 4
T_C = 0.347
L_NEW = 160
N_TRIALS = 100


def trial(L, T, offsets, seed):
    rng = np.random.default_rng(seed + 88888)
    grid = run_model(L, RHO, F_A, T, offsets, rng)
    return segregation_index(grid, offsets)


offsets = chebyshev_offsets(RADIUS)
print(f"r={RADIUS}, L={L_NEW}, T_c={T_C}, N={N_TRIALS}")
t0 = time.time()
segs = Parallel(n_jobs=-1)(
    delayed(trial)(L_NEW, T_C, offsets, seed) for seed in range(N_TRIALS)
)
segs = np.array(segs)
print(f"L={L_NEW}: Var(S) = {np.var(segs):.5f}, mean S = {np.mean(segs):.4f}")
print(f"  per-traj segs: min={segs.min():.4f}, max={segs.max():.4f}")
print(f"  bootstrap CI: ", end="")
rng = np.random.default_rng(0)
boots = [float(np.var(rng.choice(segs, len(segs), replace=True))) for _ in range(2000)]
print(f"[{np.percentile(boots, 2.5):.5f}, {np.percentile(boots, 97.5):.5f}]")
print(f"Took {time.time()-t0:.0f}s")

# Combine with prior L=40, L=80 data to fit alpha on 3 points
prior_L40 = 0.06636  # from r=4 N=200 tightening
prior_L80 = 0.11619
L_all = [40, 80, L_NEW]
V_all = [prior_L40, prior_L80, float(np.var(segs))]
log_L = np.log(np.array(L_all, dtype=float))
log_V = np.log(np.array(V_all))
alpha_3pt = float(np.polyfit(log_L, log_V, 1)[0])
print(f"\nAlpha 3-point fit (L={L_all}): {alpha_3pt:+.4f}")
print(f"Variances: L=40 {V_all[0]:.5f}, L=80 {V_all[1]:.5f}, L={L_NEW} {V_all[2]:.5f}")
print(f"L=80→L={L_NEW} slope: {(np.log(V_all[2]) - np.log(V_all[1])) / (np.log(L_NEW) - np.log(80)):+.4f}")

np.savez('outputs/data/r4_L160.npz',
         L=L_all, V=V_all, alpha_3pt=alpha_3pt, n_trials_L160=N_TRIALS, T_c=T_C)
print(f"Saved outputs/data/r4_L160.npz")
