"""Optimise microphone weights so a weighted array estimates the listener pressure.

Port of ``matlab/Sensor8_PSO.m`` / ``automated_PSO_Sensor8.m``: for each
frequency PSO finds the microphone weight vector that makes
``mean(w * p_mics)`` track the true pressure at the listener ("headrest")
position.  Reproduces the "estimated vs actual" curve without loading the
archived results.

    python examples/run_sensor_weight_pso.py [--force 800] [--freqs 40] [--iter 300] [--plot]
"""
import argparse

import numpy as np

from _paths import DATA  # noqa: F401
from acoustic_enclosure import PSOOptions, System, minimize
from acoustic_enclosure.objectives import sensor_weight_cost

DIM = (2.5, 1.3, 1.4)
# 8 microphone positions as fractions of the cabin dimensions (Sensor8_PSO.m)
MIC_FRAC = np.array([
    [0, 0, 1], [0, 1, 1], [1 / 3, 1 / 2, 1], [0, 1 / 4, 3 / 5],
    [1 / 3, 1 / 4, 1], [1 / 3, 0, 3 / 5], [1 / 3, 1, 3 / 5], [0, 1 / 2, 1 / 2],
])
LISTENER_FRAC = np.array([1 / 3, 1 / 4, 3 / 5])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", type=float, default=800.0)
    ap.add_argument("--freqs", type=int, default=40)
    ap.add_argument("--iter", type=int, default=300)
    ap.add_argument("--npop", type=int, default=30)
    ap.add_argument("--max-w", type=float, default=100.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--plot", action="store_true")
    args = ap.parse_args()

    sys = System(dim=DIM, n_cavity=70, n_plate=50)
    force_loc = np.array([13 * DIM[0] / 30, DIM[1] / 2, DIM[2]])
    mics = MIC_FRAC * DIM
    listener = LISTENER_FRAC * DIM

    freqs = np.linspace(20, 400, args.freqs)
    opt = PSOOptions(
        n_var=8,
        lower=np.zeros(8),
        upper=np.full(8, args.max_w),
        n_pop=args.npop,
        max_iter=args.iter,
        seed=args.seed,
    )

    est, act, wbest = [], [], []
    for f in freqs:
        omega = 2 * np.pi * f
        res = minimize(
            lambda w: sensor_weight_cost(w, sys, args.force, force_loc, omega, mics, listener), opt
        )
        w = res.best_position
        p_mics = sys.pressure(args.force, force_loc, omega, mics)
        p_true = sys.pressure(args.force, force_loc, omega, np.atleast_2d(listener))[0]
        est.append(abs(np.mean(w * p_mics)))
        act.append(abs(p_true))
        wbest.append(w)
        print(f"f = {f:6.1f} Hz | |estimate| {est[-1]:.4e} | |actual| {act[-1]:.4e}")

    if args.plot:
        import matplotlib.pyplot as plt

        est, act = np.array(est), np.array(act)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(freqs, 20 * np.log(est), "r", linewidth=2, label="Estimated")
        ax.plot(freqs, 20 * np.log(act), linewidth=2, label="Actual")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Pressure (dB)")
        ax.legend()
        fig.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
