"""Tighten α(r) for r=3,4,5,6 with N=200 trials per L. Bootstrap CI on α."""
import sys, os, time, numpy as np
from joblib import Parallel, delayed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from benchmarking.multiradius_experiment import (
    chebyshev_offsets, run_model, RHO, F_A, segregation_index
)

T_C_PER_R = {3: 0.334, 4: 0.347, 5: 0.374, 6: 0.402}
L_FSS = [40, 80]
N_TRIALS = 200


def trial(L, T, offsets, seed):
    rng = np.random.default_rng(seed + 12345)
    grid = run_model(L, RHO, F_A, T, offsets, rng)
    return segregation_index(grid, offsets)


def fit_alpha(samples_per_L, L_arr):
    alphas = []
    rng = np.random.default_rng(7)
    log_L = np.log(np.array(L_arr, dtype=float))
    for _ in range(2000):
        v_boot = []
        for samples in samples_per_L:
            v = np.var(rng.choice(samples, len(samples), replace=True))
            v_boot.append(v + 1e-15)
        log_v = np.log(np.array(v_boot))
        a = np.polyfit(log_L, log_v, 1)[0]
        alphas.append(a)
    return float(np.mean(alphas)), float(np.percentile(alphas, 2.5)), float(np.percentile(alphas, 97.5))


for r in (3, 4, 5, 6):
    T_c = T_C_PER_R[r]
    offsets = chebyshev_offsets(r)
    print(f"\n=== r={r}, T_c={T_c}, k={len(offsets)}, N={N_TRIALS} ===")
    samples_per_L = []
    for L in L_FSS:
        t1 = time.time()
        segs = Parallel(n_jobs=-1)(
            delayed(trial)(L, T_c, offsets, seed) for seed in range(N_TRIALS)
        )
        segs = np.array(segs)
        var = float(np.var(segs))
        mean = float(np.mean(segs))
        rng = np.random.default_rng(0)
        boots = [float(np.var(rng.choice(segs, len(segs), replace=True))) for _ in range(2000)]
        var_lo, var_hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
        print(f"  L={L}: Var(S)={var:.5f} CI95 [{var_lo:.5f}, {var_hi:.5f}], meanS={mean:.4f}, {time.time()-t1:.0f}s")
        samples_per_L.append(segs)
    alpha_mean, alpha_lo, alpha_hi = fit_alpha(samples_per_L, L_FSS)
    print(f"  alpha = {alpha_mean:+.3f}, 95% CI [{alpha_lo:+.3f}, {alpha_hi:+.3f}]")
    np.savez(f'outputs/data/r{r}_tight.npz',
             L=L_FSS, alpha_mean=alpha_mean,
             alpha_lo=alpha_lo, alpha_hi=alpha_hi, n_trials=N_TRIALS, T_c=T_c)

print("\nDone")
