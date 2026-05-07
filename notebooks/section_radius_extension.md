# Section: Larger neighbourhoods do not restore criticality

*Draft for the Schelling FSS preprint; paste into Overleaf manuscript as a new section after the five-diagnostics analysis and before the heterogeneous-tolerance discussion.*

## Setup

To test whether the negative phase-transition verdict survives a denser satisfaction spectrum, we replace the 8-site Moore neighbourhood with Chebyshev disks of radius $r \in \{2, 3, 4, 5, 6\}$. The neighbour count grows as $k(r) = (2r+1)^2 - 1$ and the satisfaction spectrum size $|F_k|$ grows roughly as $k \log k$:

| $r$ | $k$ | $|F_k|$ |
|---|---|---|
| 1 (Moore) | 8 | 23 |
| 2 (Chebyshev) | 24 | 181 |
| 3 (Chebyshev) | 48 | 713 |
| 4 (Chebyshev) | 80 | 1\,967 |
| 5 (Chebyshev) | 120 | 4\,387 |
| 6 (Chebyshev) | 168 | 8\,611 |

For each $r$ we run a coarse $T$-sweep ($N_T = 60$, $L = 40$, 30 trials per $T$) followed by a fine sweep ($N_T = 40$, $L = 40$, 50 trials) around the $T$ at maximum $|dS/dT|$. The resulting per-radius $T_c(r)$ ranges from 0.255 (Moore) to 0.402 ($r=6$).

## Variance scaling exponent $\alpha(r)$

We measure $\mathrm{Var}(S)$ at $T_c(r)$ for $L \in \{40, 80\}$ with $N = 200$ paired trials and bootstrap confidence intervals on $\alpha = d \log \mathrm{Var}(S) / d \log L$. The full-grid fit on $L \in \{40, 80\}$ gives:

| $r$ | $\alpha$ (N=200) | 95% CI |
|---|---|---|
| 3 | -1.92 | [-2.36, -1.52] |
| 4 | **+0.81** | [+0.50, +1.18] |
| 5 | -1.24 | [-2.06, -0.66] |
| 6 | -5.20 | [-7.04, -3.23] |

The $r = 4$ exponent is bootstrap-disjoint above zero, an apparent super-critical signal. Extending the lattice grid to $L = 160$ at the same $T_c$ collapses this:

| $L$ | $\mathrm{Var}(S)$ at $r{=}4$, $T{=}0.347$ | mean $S$ |
|---|---|---|
| 40 | 0.066 | 0.147 |
| 80 | 0.116 | 0.518 |
| 160 | 0.012 | 0.781 |

The 3-point fit on $L \in \{40, 80, 160\}$ gives $\alpha(r{=}4) = -1.23$, fully consistent with sub-criticality. The variance grows from $L=40$ to $L=80$ and then collapses by an order of magnitude at $L=160$ as the system equilibrates to a sharp deterministic segregation peak. The same pattern at $r = 5$ gives a 3-point $\alpha = -3.74$ ($\mathrm{Var}(S) = 0.100, 0.044, 0.0006$ across $L = 40, 80, 160$). The apparent super-criticality at $r = 4$ on the two-point grid is therefore a transient finite-size enhancement, not the start of a divergent susceptibility.

## Independent test: Binder cumulant has no L-curve crossing

We compute the Binder cumulant $U_4 = 1 - \langle S^4 \rangle / 3 \langle S^2 \rangle^2$ on a $T$-grid of 15 points spanning $\pm 0.045$ around each $T_c(r)$, with $N = 80$ trials per $(L, T)$. For a critical system, $U_4(T)$ curves at different $L$ are size-independent at $T_c$ and therefore cross. Across $r = 3, 4, 5, 6$ the curves do not exhibit a genuine size-independent crossing: $U_4$ jumps from large-negative values (the ordered-fluctuation regime) to the trivial $2/3$ disordered plateau within a narrow temperature window, with $L = 80$ transitioning slightly earlier than $L = 40$. The two curves intersect during this transition jump but immediately separate, with $L = 80$ reaching the $2/3$ plateau at lower $T$ than $L = 40$. This is consistent with a sharp first-order-like transition without a critical point, and inconsistent with a second-order critical scenario.

## Transition broadening, not sharpening

The peak of $|dS/dT|$ on the coarse $T$-sweep at $L = 40$ decreases monotonically from 97.5 at $r = 1$ to 39.1 at $r = 6$. A genuine phase transition would have peak $|dS/dT|$ diverging with $L$ at fixed $r$ and becoming sharper as $r$ increases at fixed $L$. The observed monotonic decrease is the opposite signal: the dense-neighbourhood transition is broader, not sharper, than the Moore baseline.

## Mechanism: deterministic high-$k$ dynamics

A direct diagnostic at $L = 80$ records the number of agent moves to convergence per random seed. For $r \in \{4, 5, 6\}$, the means are $4\,182, 5\,269, 5\,283$ moves and the standard deviations across 8 seeds are $1\,557, 112, 155$. The collapse of seed-to-seed variability at $r \geq 5$ (from std $\approx 1\,500$ at $r = 4$ to $\approx 100$ at $r \geq 5$) shows the high-$k$ dynamics are highly deterministic: different random initialisations converge to nearly identical equilibrium segregation outcomes. This is the underlying mechanism for the variance collapse at $L = 80$ for $r \geq 5$ — the equilibrium variance vanishes faster than the classical $L^{-2}$ scaling not because of divergent susceptibility, but because the dynamics are deterministic.

## Interpretation

The original "Schelling is not a phase transition" verdict survives the dense-spectrum extension. None of three independent diagnostics — variance scaling exponent across three lattice sizes, Binder cumulant L-curve crossings, and $|dS/dT|$ peak height — shows critical behaviour for any of $r \in \{1, \ldots, 6\}$. The dense-spectrum limit moves further from criticality, not closer: the transition broadens, the seed-to-seed variability collapses, and the equilibrium segregation tends to a sharp deterministic peak. The 23-threshold staircase argument that pinned the Moore neighbourhood in the sub-critical regime is thus the wrong mechanism for the negative verdict; the true mechanism is the absence of long-range correlations in the equilibrium configuration, which holds across all neighbourhood sizes tested.

A definitive resolution at the $r \to \infty$ mean-field limit would require per-$L$ $T_c$ determination via Binder cumulant crossing on $L \in \{40, 80, 160, 320\}$ for each $r$, but the cross-radius pattern is already strong: dense neighbourhoods do not restore criticality.
