"""Optimise two secondary-source positions/strengths to minimise zone energy.

Port of ``matlab/PSO_2Speaker_Pressure_Min.m``: for each excitation frequency,
PSO searches the 8-D vector ``[x1 y1 z1 q1  x2 y2 z2 q2]`` to minimise the
acoustic potential energy in a small target zone near a cabin corner.

    python examples/run_speaker_placement_pso.py [--freqs 6] [--iter 300] [--plot]

This is a genuine optimisation run (no stored results), so it is slower than the
plotting examples – lower ``--freqs`` / ``--iter`` for a quick look.
"""
import argparse

import numpy as np

from _paths import DATA  # noqa: F401  (keeps sys.path patched)
from acoustic_enclosure import PSOOptions, System, TargetZone, minimize
from acoustic_enclosure.objectives import speaker_placement_cost


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--freqs", type=int, default=6)
    ap.add_argument("--iter", type=int, default=300)
    ap.add_argument("--npop", type=int, default=30)
    ap.add_argument("--force", type=float, default=1000.0)
    ap.add_argument("--max-q", type=float, default=10.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--plot", action="store_true")
    ap.add_argument("--mesh", type=int, nargs=3, metavar=("NX", "NY", "NZ"),
                    default=(60, 40, 30),
                    help="integration mesh (MATLAB used 120 80 60; coarser is much faster)")
    args = ap.parse_args()

    dim = (2.5, 1.3, 1.4)
    sys = System(dim=dim, n_cavity=70, n_plate=50)
    force_loc = np.array([13 * dim[0] / 30, dim[1] / 2, dim[2]])
    zone = TargetZone.default(dim, nx=args.mesh[0], ny=args.mesh[1], nz=args.mesh[2]).prepare(sys)

    freqs = np.linspace(20, 400, args.freqs)
    single_max = [dim[0], dim[1], dim[2], args.max_q]
    opt = PSOOptions(
        n_var=8,
        lower=np.zeros(8),
        upper=np.tile(single_max, 2),
        n_pop=args.npop,
        max_iter=args.iter,
        seed=args.seed,
    )

    rows = []
    for f in freqs:
        omega = 2 * np.pi * f
        baseline = speaker_placement_cost(np.zeros(8), sys, args.force, force_loc, omega, zone)
        res = minimize(
            lambda x: speaker_placement_cost(x, sys, args.force, force_loc, omega, zone), opt
        )
        reduction_db = 10 * np.log10(res.best_cost / baseline)
        rows.append((f, baseline, res.best_cost, reduction_db, res.best_position))
        print(
            f"f = {f:6.1f} Hz | energy {baseline:.3e} -> {res.best_cost:.3e} "
            f"({reduction_db:+.1f} dB) | src1 {res.best_position[:3].round(2)} "
            f"src2 {res.best_position[4:7].round(2)}"
        )

    if args.plot:
        import matplotlib.pyplot as plt

        f = [r[0] for r in rows]
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(f, [10 * np.log10(r[1]) for r in rows], "o-", label="no control")
        ax.plot(f, [10 * np.log10(r[2]) for r in rows], "s-", label="PSO-optimised")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Zone acoustic energy (dB)")
        ax.legend()
        fig.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
