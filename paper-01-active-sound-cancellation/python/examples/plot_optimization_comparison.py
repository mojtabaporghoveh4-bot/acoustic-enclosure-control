"""Convergence comparison of PSO / GA / BA / GWO.

Port of ``matlab/plotter_optimization_comparison.m``. The digitised per-algorithm
convergence traces live in ``data/optimization_comparison/`` as both the original
``.xlsx`` and dependency-free ``.csv``.

As in the MATLAB original, the BA iteration column is used as the common x-axis
for every series and the x-axis is logarithmic.

    python examples/plot_optimization_comparison.py [--save out.png]
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from _paths import DATA

DATADIR = DATA / "optimization_comparison"
SERIES = [("PSO", "Data_PSO"), ("GA", "Data_GA"), ("BA", "Data_BA"), ("GWO", "Data_GWO")]


def load(stem):
    return np.loadtxt(DATADIR / f"{stem}.csv", delimiter=",", skiprows=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--save")
    args = ap.parse_args()

    x = load("Data_BA")[:, 0]  # common x-axis, matching the MATLAB script
    with np.errstate(divide="ignore"):
        logx = np.log(x)
    keep = np.isfinite(logx)  # MATLAB silently drops the log(0) point at iteration 0
    fig, ax = plt.subplots(figsize=(6, 4))
    for label, stem in SERIES:
        ax.plot(logx[keep], load(stem)[keep, 1], linewidth=2, label=label)

    ax.set_xlabel("Logarithmic iteration")
    ax.set_ylabel("Best value")
    ax.legend()
    ax.tick_params(labelsize=11)
    for s in ax.spines.values():
        s.set_linewidth(2)
    fig.tight_layout()

    if args.save:
        fig.savefig(args.save, dpi=150)
        print("wrote", args.save)
    else:
        plt.show()


if __name__ == "__main__":
    main()
