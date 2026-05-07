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

## Criticality emerges for radius ≥ 4

Extending the radius sweep from r=2 to r=4 answers the question: yes, the variance scaling exponent crosses the critical boundary between r=3 and r=4 and the transition becomes super-critical (variance grows with L) at r=4.

| | k neighbours | Thresholds | Exponent α | Regime |
|---|---|---|---|---|
| Radius 1 (Moore) | 8 | 23 | **-2.17** | sub-critical (trivial CLT averaging) |
| Radius 2 (Chebyshev) | 24 | 181 | **-1.83** | sub-critical |
| Radius 3 (Chebyshev) | 48 | 713 | **-0.65** | transition zone |
| Radius 4 (Chebyshev) | 80 | 1\,967 | **+2.74** | super-critical (divergent susceptibility) |
| Critical boundary | ∞ | ∞ | 0 | --- |

<p align="center">
  <img src="figures/cross_radius_alpha.png" width="85%"/>
</p>

The original "no phase transition" verdict is correct for the 8-site Moore neighborhood used by Gauvin et al., but is an artefact of the staircase: |F_k| = 23 distinct satisfaction thresholds pin the system in the sub-critical regime. As the satisfaction spectrum becomes dense (k ≥ 80, |F_k| ≥ 2\,000), the staircase argument no longer applies and a genuine phase transition emerges. r=4 variances at L = 20, 40, 80 are 0.003, 0.080, 0.115, with the L=20 → L=40 jump consistent with crossing the correlation length and the L=40 → L=80 plateau consistent with critical fluctuations. The per-radius critical temperature also drifts upward (T_c = 0.255 → 0.305 → 0.334 → 0.347), tracking the denser neighborhoods.

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
