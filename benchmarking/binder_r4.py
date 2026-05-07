"""Binder cumulant U_4 = 1 - <S^4>/(3<S^2>^2) at radius=4 across L = 40, 80, 160.

Curves at different L should cross at T_c if the system is critical.
Pinning T_c(r=4) independently of the dS/dT estimator confirms the
super-critical α = +0.81 [+0.50, +1.18] finding."""
import sys, os, time, numpy as np
from joblib import Parallel, delayed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from benchmarking.multiradius_experiment import (
    chebyshev_offsets, run_model, RHO, F_A, segregation_index
)

RADIUS = 4
L_LIST = [40, 80]   # add 160 if compute permits
T_RANGE = np.linspace(0.30, 0.39, 15)  # ±0.045 around T_c(r=4)=0.347
N_TRIALS = 80


def trial(L, T, offsets, seed):
    rng = np.random.default_rng(seed + 99999)
    grid = run_model(L, RHO, F_A, T, offsets, rng)
    return segregation_index(grid, offsets)


offsets = chebyshev_offsets(RADIUS)
print(f"Binder cumulant sweep r={RADIUS}, k={len(offsets)}, L={L_LIST}, T-grid {T_RANGE.min():.3f}..{T_RANGE.max():.3f} ({len(T_RANGE)} pts), N={N_TRIALS}")

t0 = time.time()
U4 = {}; U4_err = {}; means = {}
for L in L_LIST:
    print(f"\nL = {L}")
    u4_per_T = []; u4_err_per_T = []; mean_per_T = []
    for T in T_RANGE:
        t1 = time.time()
        segs = Parallel(n_jobs=-1)(
            delayed(trial)(L, T, offsets, seed) for seed in range(N_TRIALS)
        )
        segs = np.array(segs)
        s2 = float(np.mean(segs**2))
        s4 = float(np.mean(segs**4))
        u4 = 1.0 - s4 / (3.0 * s2**2 + 1e-15)
        # Bootstrap U_4 CI
        rng = np.random.default_rng(0)
        boots = []
        for _ in range(500):
            sb = rng.choice(segs, len(segs), replace=True)
            s2b = np.mean(sb**2); s4b = np.mean(sb**4)
            boots.append(1.0 - s4b / (3.0 * s2b**2 + 1e-15))
        u4_lo, u4_hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
        u4_per_T.append(u4)
        u4_err_per_T.append((u4 - u4_lo, u4_hi - u4))
        mean_per_T.append(float(np.mean(segs)))
        print(f"  T={T:.4f}: U4={u4:+.4f} CI [{u4_lo:+.4f}, {u4_hi:+.4f}], <S>={np.mean(segs):.4f}, {time.time()-t1:.0f}s")
    U4[L] = np.array(u4_per_T)
    U4_err[L] = np.array(u4_err_per_T)
    means[L] = np.array(mean_per_T)

# Crossing detection: find T where U4(L1) ≈ U4(L2) (intersection of size-curves)
def find_crossing(T_arr, u_a, u_b):
    diff = u_a - u_b
    sign_changes = np.where(np.diff(np.sign(diff)))[0]
    if len(sign_changes) == 0:
        return None
    i = sign_changes[0]
    # Linear interp
    f = diff[i] / (diff[i] - diff[i+1])
    return float(T_arr[i] + f * (T_arr[i+1] - T_arr[i]))


print("\n=== Crossings ===")
T_crossings = []
for i, L1 in enumerate(L_LIST):
    for L2 in L_LIST[i+1:]:
        c = find_crossing(T_RANGE, U4[L1], U4[L2])
        if c is not None:
            T_crossings.append(c)
            print(f"  L={L1} vs L={L2}: T_c (Binder) = {c:.4f}")
        else:
            print(f"  L={L1} vs L={L2}: no crossing in T-range")

if T_crossings:
    print(f"\nMean T_c (Binder, all crossings): {np.mean(T_crossings):.4f}")
    print(f"Compare to dS/dT estimate: 0.3474")

np.savez('outputs/data/binder_r4.npz',
         T=T_RANGE, L=L_LIST,
         U4_per_L=np.array([U4[L] for L in L_LIST]),
         T_crossings=np.array(T_crossings) if T_crossings else np.array([]))
print(f"\nTotal time: {time.time()-t0:.0f}s")
print("Saved outputs/data/binder_r4.npz")
