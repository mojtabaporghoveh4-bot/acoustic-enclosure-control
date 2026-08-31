"""Particle Swarm Optimisation with constriction coefficients.

Direct port of ``Best_PSO_COMPLETED.m`` – the variant selected as the best
performer in the optimisation comparison (see
``examples/plot_optimization_comparison.py``).

It uses Clerc & Kennedy constriction (``phi1 = phi2 = 2.05``), velocity clamping
at 10 % of the search range, and reflecting walls with position clamping.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

__all__ = ["PSOOptions", "PSOResult", "minimize"]


@dataclass
class PSOOptions:
    n_var: int
    lower: np.ndarray            # (n_var,) lower bounds
    upper: np.ndarray            # (n_var,) upper bounds
    n_pop: int = 30              # swarm size          (opt.Npop)
    max_iter: int = 200          # iterations          (opt.Iter)
    phi1: float = 2.05           # cognitive parameter
    phi2: float = 2.05           # social parameter
    w_damp: float = 1.0          # inertia damping per iteration
    seed: int | None = None

    def __post_init__(self):
        self.lower = np.broadcast_to(np.asarray(self.lower, float), (self.n_var,)).copy()
        self.upper = np.broadcast_to(np.asarray(self.upper, float), (self.n_var,)).copy()


@dataclass
class PSOResult:
    best_cost: float
    best_position: np.ndarray
    history: np.ndarray = field(repr=False)   # (max_iter,) global best per iteration


def minimize(cost: Callable[[np.ndarray], float], opt: PSOOptions) -> PSOResult:
    """Minimise ``cost(x)`` over the box ``[opt.lower, opt.upper]``."""
    rng = np.random.default_rng(opt.seed)

    phi = opt.phi1 + opt.phi2
    chi = 2.0 / (phi - 2.0 + np.sqrt(phi ** 2 - 4.0 * phi))
    w = chi
    c1 = chi * opt.phi1
    c2 = chi * opt.phi2

    vmax = 0.1 * (opt.upper - opt.lower)
    vmin = -vmax

    pos = rng.uniform(opt.lower, opt.upper, size=(opt.n_pop, opt.n_var))
    vel = np.zeros_like(pos)
    cost_val = np.array([cost(p) for p in pos])

    pbest_pos = pos.copy()
    pbest_cost = cost_val.copy()

    g = int(np.argmin(pbest_cost))
    gbest_pos = pbest_pos[g].copy()
    gbest_cost = float(pbest_cost[g])

    history = np.zeros(opt.max_iter)
    for it in range(opt.max_iter):
        for i in range(opt.n_pop):
            vel[i] = (
                w * vel[i]
                + c1 * rng.random(opt.n_var) * (pbest_pos[i] - pos[i])
                + c2 * rng.random(opt.n_var) * (gbest_pos - pos[i])
            )
            np.clip(vel[i], vmin, vmax, out=vel[i])

            pos[i] = pos[i] + vel[i]

            outside = (pos[i] < opt.lower) | (pos[i] > opt.upper)
            vel[i][outside] = -vel[i][outside]
            np.clip(pos[i], opt.lower, opt.upper, out=pos[i])

            ci = cost(pos[i])
            if ci < pbest_cost[i]:
                pbest_cost[i] = ci
                pbest_pos[i] = pos[i].copy()
                if ci < gbest_cost:
                    gbest_cost = float(ci)
                    gbest_pos = pos[i].copy()

        history[it] = gbest_cost
        w *= opt.w_damp

    return PSOResult(best_cost=gbest_cost, best_position=gbest_pos, history=history)
