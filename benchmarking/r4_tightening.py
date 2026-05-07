"""Tighten α(r=4) estimate with N=200 trials per L."""
import sys, os, time, numpy as np
from joblib import Parallel, delayed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.schelling import EMPTY, TYPE_A, TYPE_B
from benchmarking.multiradius_experiment import (
    chebyshev_offsets, init_grid, run_model, RHO, F_A, segregation_index
)

T_C = 0.347   # from prior r=4 fine-sweep
RADIUS = 4
N_TRIALS = 200
L_FSS = [40, 80]  # apples-to-apples with r=5/r=6


def trial(L, T, offsets, seed):
    rng = np.random.default_rng(seed + 12345)
    grid = run_model(L, RHO, F_A, T, offsets, rng)
    return segregation_index(grid, offsets)


offsets = chebyshev_offsets(RADIUS)
print(f"r={RADIUS}, T_c={T_C}, N_TRIALS={N_TRIALS}")

t0 = time.time()
variances = []
seg_means = []
for L in L_FSS:
    t1 = time.time()
    segs = Parallel(n_jobs=-1)(
        delayed(trial)(L, T_C, offsets, seed) for seed in range(N_TRIALS)
    )
    var = float(np.var(segs))
    mean = float(np.mean(segs))
    # Bootstrap CI on variance
    rng = np.random.default_rng(0)
    boots = [float(np.var(rng.choice(segs, len(segs), replace=True))) for _ in range(2000)]
    var_lo, var_hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
    variances.append((L, var, var_lo, var_hi, mean))
    print(f"  L={L}: Var(S)={var:.5f} CI95 [{var_lo:.5f}, {var_hi:.5f}], mean S={mean:.4f}, took {time.time()-t1:.0f}s")

# Bootstrap α
def fit_alpha(samples_per_L):
    alphas = []
    rng = np.random.default_rng(7)
    for _ in range(2000):
        v_boot = []
        for samples in samples_per_L:
            v = np.var(rng.choice(samples, len(samples), replace=True))
            v_boot.append(v)
        log_L = np.log(np.array([L for L, _, _, _, _ in variances], dtype=float))
        log_v = np.log(np.array(v_boot) + 1e-15)
        a = np.polyfit(log_L, log_v, 1)[0]
        alphas.append(a)
    return float(np.mean(alphas)), float(np.percentile(alphas, 2.5)), float(np.percentile(alphas, 97.5))


# We need samples per L. Re-run trials and store per-trial.
samples_per_L = []
for L in L_FSS:
    segs = Parallel(n_jobs=-1)(
        delayed(trial)(L, T_C, offsets, seed) for seed in range(N_TRIALS)
    )
    samples_per_L.append(np.array(segs))

alpha_mean, alpha_lo, alpha_hi = fit_alpha(samples_per_L)
print(f"\nalpha = {alpha_mean:+.3f}, 95% CI [{alpha_lo:+.3f}, {alpha_hi:+.3f}]")
print(f"Total time: {time.time() - t0:.0f}s")

np.savez('outputs/data/r4_tight.npz',
         L=L_FSS, vars=[v[1] for v in variances], var_lo=[v[2] for v in variances],
         var_hi=[v[3] for v in variances], alpha_mean=alpha_mean,
         alpha_lo=alpha_lo, alpha_hi=alpha_hi, n_trials=N_TRIALS, T_c=T_C)
print(f"Saved outputs/data/r4_tight.npz")
