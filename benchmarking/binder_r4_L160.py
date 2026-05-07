"""Binder cumulant U_4 at radius=4 across L = 40, 80, 160 for definitive crossing test.

The L=160 panel is the decisive test: if L=160 curve crosses or runs above
L=40, L=80 at any T, criticality is alive. If L=160 sits BELOW L=40 and L=80
across the whole T-range (and especially at the L=40-determined T_c=0.347),
the no-criticality verdict is definitive."""
import sys, os, time, numpy as np
from joblib import Parallel, delayed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from benchmarking.multiradius_experiment import (
    chebyshev_offsets, run_model, RHO, F_A, segregation_index
)

RADIUS = 4
L_LIST = [40, 80, 160]
T_RANGE = np.linspace(0.32, 0.39, 12)
N_TRIALS = 60


def trial(L, T, offsets, seed):
    rng = np.random.default_rng(seed + 99999)
    grid = run_model(L, RHO, F_A, T, offsets, rng)
    return segregation_index(grid, offsets)


offsets = chebyshev_offsets(RADIUS)
print(f"r={RADIUS}, L={L_LIST}, T-range {T_RANGE.min():.3f}..{T_RANGE.max():.3f} ({len(T_RANGE)} pts), N={N_TRIALS}")

t0 = time.time()
U4 = {}; means_S = {}
for L in L_LIST:
    print(f"\nL={L}")
    u4_per_T = []; mean_per_T = []
    for T in T_RANGE:
        t1 = time.time()
        segs = Parallel(n_jobs=-1)(
            delayed(trial)(L, T, offsets, seed) for seed in range(N_TRIALS)
        )
        segs = np.array(segs)
        s2 = float(np.mean(segs**2))
        s4 = float(np.mean(segs**4))
        u4 = 1.0 - s4 / (3.0 * s2**2 + 1e-15)
        u4_per_T.append(u4)
        mean_per_T.append(float(np.mean(segs)))
        print(f"  T={T:.4f}: U4={u4:+.4f}, <S>={np.mean(segs):.4f}, var(S)={float(np.var(segs)):.5f}, took {time.time()-t1:.0f}s")
    U4[L] = np.array(u4_per_T)
    means_S[L] = np.array(mean_per_T)


# Find any T where U4(L1) ≈ U4(L2) ≈ U4(L3) (3-curve crossing point)
print("\n=== L-pair crossings ===")
def find_crossing(T_arr, u_a, u_b):
    diff = u_a - u_b
    sign_changes = np.where(np.diff(np.sign(diff)))[0]
    if len(sign_changes) == 0:
        return None
    i = sign_changes[0]
    if (diff[i] - diff[i+1]) == 0:
        return None
    f = diff[i] / (diff[i] - diff[i+1])
    return float(T_arr[i] + f * (T_arr[i+1] - T_arr[i]))


for i, L1 in enumerate(L_LIST):
    for L2 in L_LIST[i+1:]:
        c = find_crossing(T_RANGE, U4[L1], U4[L2])
        if c is not None:
            print(f"  L={L1} vs L={L2}: U4 crossing at T = {c:.4f}")
        else:
            print(f"  L={L1} vs L={L2}: no crossing in T-range")

# Sanity check: is U_4 plateau height near 2/3 for all L?
print(f"\nPlateau heights at T=max ({T_RANGE[-1]:.3f}):")
for L in L_LIST:
    print(f"  L={L}: U4={U4[L][-1]:+.4f}, <S>={means_S[L][-1]:.4f}")

np.savez('outputs/data/binder_r4_L160.npz',
         T=T_RANGE, L=L_LIST,
         U4_per_L=np.array([U4[L] for L in L_LIST]),
         meanS_per_L=np.array([means_S[L] for L in L_LIST]))
print(f"\nTotal time: {time.time()-t0:.0f}s")
print("Saved outputs/data/binder_r4_L160.npz")
