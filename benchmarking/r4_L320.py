"""Extend r=4 FSS to L=320 — the deepest L-grid evidence for/against criticality."""
import sys, os, time, numpy as np
from joblib import Parallel, delayed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from benchmarking.multiradius_experiment import (
    chebyshev_offsets, run_model, RHO, F_A, segregation_index
)

RADIUS = 4
T_C = 0.347
L_NEW = 320
N_TRIALS = 50  # L=320 is ~16x slower than L=80 per trial


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
v_320 = float(np.var(segs))
m_320 = float(np.mean(segs))
print(f"L={L_NEW}: Var(S)={v_320:.6f}, mean S={m_320:.4f}")
rng = np.random.default_rng(0)
boots = [float(np.var(rng.choice(segs, len(segs), replace=True))) for _ in range(2000)]
v_lo, v_hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
print(f"  bootstrap CI Var(S): [{v_lo:.6f}, {v_hi:.6f}]")
print(f"Took {time.time()-t0:.0f}s")

# Combine with prior L=40, L=80, L=160
v_40, v_80, v_160 = 0.06636, 0.11619, 0.01204  # from r=4 N=200 + L=160 runs
L_all = [40, 80, 160, L_NEW]
V_all = [v_40, v_80, v_160, v_320]
log_L = np.log(np.array(L_all, dtype=float))
log_V = np.log(np.array(V_all))
alpha_4pt = float(np.polyfit(log_L, log_V, 1)[0])
print(f"\nVariances: L=40={v_40:.5f}, L=80={v_80:.5f}, L=160={v_160:.5f}, L={L_NEW}={v_320:.5f}")
print(f"Slopes: 40→80={float(np.log(v_80/v_40)/np.log(80/40)):+.3f}, "
      f"80→160={float(np.log(v_160/v_80)/np.log(160/80)):+.3f}, "
      f"160→{L_NEW}={float(np.log(v_320/v_160)/np.log(L_NEW/160)):+.3f}")
print(f"4-point fit α(L=40,80,160,320) = {alpha_4pt:+.4f}")

np.savez('outputs/data/r4_L320.npz',
         L=L_all, V=V_all, alpha_4pt=alpha_4pt, n_trials_L320=N_TRIALS, T_c=T_C,
         var_L320_ci=(v_lo, v_hi))
print(f"Saved outputs/data/r4_L320.npz")
