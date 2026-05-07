"""Diagnose the high-k frozen-equilibrium hypothesis.

Run r=4 and r=5 at L=80, T=Tc(r), record # of step iterations until
the system freezes (no unsatisfied agents). If r=5 freezes within
< 50 steps while r=4 takes hundreds, hypothesis confirmed."""
import sys, os
import numpy as np
from joblib import Parallel, delayed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.schelling import EMPTY, TYPE_A, TYPE_B
from benchmarking.multiradius_experiment import (
    chebyshev_offsets, init_grid, step, RHO, F_A
)

T_C_PER_R = {4: 0.347, 5: 0.374, 6: 0.402}
L = 80
N_TRIALS = 8
MAX_STEPS = 1000


def run_with_log(L, T, offsets, seed):
    rng = np.random.default_rng(seed)
    grid = init_grid(L, RHO, F_A, rng)
    moves_per_step = []
    for s in range(MAX_STEPS):
        m = step(grid, L, T, offsets, rng)
        moves_per_step.append(m)
        if m == 0:
            return s + 1, moves_per_step
    return MAX_STEPS, moves_per_step


for r in (4, 5, 6):
    T_c = T_C_PER_R[r]
    offsets = chebyshev_offsets(r)
    print(f"\n=== r={r}, k={len(offsets)}, L={L}, T={T_c} ===")
    results = Parallel(n_jobs=-1)(
        delayed(run_with_log)(L, T_c, offsets, seed) for seed in range(N_TRIALS)
    )
    iters = [res[0] for res in results]
    total_moves_per_run = [sum(res[1]) for res in results]
    print(f"Iters to convergence: mean={np.mean(iters):.1f}, std={np.std(iters):.1f}, min={min(iters)}, max={max(iters)}")
    print(f"Total moves per run:  mean={np.mean(total_moves_per_run):.0f}, std={np.std(total_moves_per_run):.0f}")
    print(f"  (cells in grid: {L*L})")
