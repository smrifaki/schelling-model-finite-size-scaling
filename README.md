# Finite-Size Scaling Analysis of the Schelling Segregation Model

[Gauvin et al. (2009)](https://doi.org/10.1140/epjb/e2009-00234-0) ran finite-size scaling on Schelling grids up to L=60 and reported exponents consistent with the 2D Ising universality class. We ran the same analysis on grids up to **L=320** with **50 trials per point** (12,500+ simulations distributed across 20 CI workers) and reached a different conclusion:

**Every scaling diagnostic fails. The Schelling transition is not a phase transition.**

<p align="center">
  <img src="figures/grid_snapshots.png" width="85%"/>
</p>

## Why it fails: the 23-threshold staircase

The Moore neighborhood has 8 sites. Agent satisfaction is always a ratio j/k with k ≤ 8. The set of achievable values is

$$\mathcal{F}_8 = \bigcup_{k=1}^{8} \{j/k : 0 \leq j \leq k\}$$

which contains exactly **23 distinct elements**. We prove (Theorem 2.1) that for a fixed random seed, the equilibrium segregation index S(T) is piecewise constant with jumps only at these 23 thresholds. The "transition" is a staircase, not a singularity.

<p align="center">
  <img src="figures/tolerance_sweep.png" width="85%"/>
</p>

## Five diagnostics, five failures

| | Critical system | Schelling (Moore) |
|---|---|---|
| **T_c drift** | T_c(L) → T_c^∞ as L → ∞ | No drift: all five sizes give T_c ∈ [0.271, 0.278] |
| **Variance** | L^{-γ/ν} with γ/ν > 0 | L^{-2.02 ± 0.09} (trivial CLT averaging) |
| **Susceptibility** | Diverges with L | Flat |
| **Binder cumulant** | Universal crossing point | Crossings drift, converge to trivial 2/3 plateau |
| **Data collapse** | Finite optimum for 1/ν | No finite optimum |

<p align="center">
  <img src="figures/susceptibility.png" width="48%"/>
  <img src="figures/binder_cumulant.png" width="48%"/>
</p>
<p align="center">
  <img src="figures/scaling_collapse.png" width="48%"/>
  <img src="figures/order_parameter_exponent.png" width="48%"/>
</p>
<p align="center"><sub>Susceptibility (top left), Binder cumulant (top right), scaling collapse (bottom left), variance scaling (bottom right). None behave as expected for a critical system.</sub></p>

## The mechanism: subcritical cascades

When an agent leaves, its same-type neighbors lose one like neighbor and may become unsatisfied themselves. We derive a branching ratio R(T) from first principles and predict cascade sizes of 1/(1-R). Perturbation experiments on equilibrated L=80 grids confirm this to **within 15%** for T ≤ 0.325. Above that, cascades overlap and the mean-field prediction breaks down.

The transition is driven by rare large cascades in the tail. The median cascade size is 1 at all T.

## Finite correlation length

<p align="center">
  <img src="figures/multiscalar_trajectories.png" width="48%"/>
  <img src="figures/trajectory_statistics.png" width="48%"/>
</p>

The [multiscalar dissimilarity](https://doi.org/10.1177/2399808319830645) characteristic length r* stays between 3 and 6 lattice spacings across the entire transition. No divergence. The domains are patchy, not fractal.

## Criticality emerges for radius ≥ 3-4

Extending the radius sweep from r=2 to r=6 shows the variance scaling exponent crosses the critical boundary between r=3 and r=4. Beyond r=4 the equilibrium estimator becomes unreliable (see caveat below), but the qualitative emergence of criticality is robust.

| r | k neighbours | Thresholds | T_c | Exponent α | Regime |
|---|---|---|---|---|---|
| 1 (Moore) | 8 | 23 | 0.255 | **-2.17** | sub-critical (trivial CLT averaging) |
| 2 (Chebyshev) | 24 | 181 | 0.305 | **-1.83** | sub-critical |
| 3 (Chebyshev) | 48 | 713 | 0.334 | **-0.65** | transition zone |
| 4 (Chebyshev) | 80 | 1\,967 | 0.347 | **+2.74** | super-critical (divergent susceptibility) |
| 5 (Chebyshev) | 120 | 4\,387 | 0.374 | -6.87 | frozen-equilibrium artefact |
| 6 (Chebyshev) | 168 | 8\,611 | 0.402 | -6.14 | frozen-equilibrium artefact |
| Critical boundary | ∞ | ∞ | --- | 0 | --- |

<p align="center">
  <img src="figures/cross_radius_alpha.png" width="85%"/>
</p>

The original "no phase transition" verdict is correct for the 8-site Moore neighborhood used by Gauvin et al., but is an artefact of the staircase: |F_k| = 23 distinct satisfaction thresholds pin the system in the sub-critical regime. As the satisfaction spectrum becomes dense (k ≥ 80, |F_k| ≥ 2\,000), the staircase argument no longer applies and a genuine phase transition emerges between r=3 and r=4. The per-radius critical temperature drifts upward monotonically (T_c = 0.255 → 0.305 → 0.334 → 0.347 → 0.374 → 0.402), tracking the denser neighbourhoods.

**Caveat for r ≥ 5.** At high k the L=80 variance is anomalously small (0.001 vs 0.10 at L=40). A direct diagnostic at L=80, T_c (Phase QBI) confirms this is not a "frozen near init" artefact: the system makes ~ 5\,000 agent moves to converge for r ∈ {4, 5, 6} (vs L\^2 = 6\,400 cells). Instead, the std of total moves per run drops from 1\,557 at r=4 to 112 at r=5 and 155 at r=6, meaning the high-k dynamics are highly deterministic — different random seeds converge to the same segregation outcome. Whether this reflects (i) anomalous critical scaling with α more negative than the classical -2, (ii) effective mean-field behaviour with α ≈ -4, or (iii) a misalignment between the L=40-determined T_c and the L=80 susceptibility peak, requires per-L T_c determination via Binder cumulant crossing.

## Heterogeneous tolerance

<p align="center">
  <img src="figures/heterogeneous_comparison.png" width="48%"/>
  <img src="figures/heterogeneous_tc.png" width="48%"/>
</p>

When tolerance is drawn from Beta(κ/2, κ/2), the intolerant tail drives segregation even at moderate population-average tolerance. The transition shifts leftward for small κ. This is consistent with [empirical observations](https://doi.org/10.1073/pnas.0708155105) that segregation persists in cities where surveys indicate majority support for integration.

## Reproducing the results

```
src/
  schelling.py            Model: Moore neighborhood, periodic BC, vectorized satisfaction
  spatial_analysis.py     Multiscalar dissimilarity (Randon-Furling et al. 2020)
  phase_diagram.py        Binder cumulant, susceptibility, variance scaling, data collapse
  utils.py                Helpers

benchmarking/
  ci_worker.py            Distributed sweep worker (GitHub Actions, 20 parallel jobs)
  ci_merge.py             Aggregate chunks into ensemble statistics
  cascade_experiment.py   Perturbation cascade BFS measurement
  radius2_experiment.py   24-neighbor Chebyshev variant

tests/                    94 tests across 4 modules
```

```bash
pip install -e ".[dev]"
make test     # 94 tests
make bench    # full parameter sweeps
make plots    # regenerate all figures
```

<p align="center">
  <img src="figures/finite_size_curves.png" width="85%"/>
</p>
<p align="center"><sub>S(T) for L = 20 to 320. The curves steepen but do not shift. At L=320 the staircase structure is unambiguous.</sub></p>
