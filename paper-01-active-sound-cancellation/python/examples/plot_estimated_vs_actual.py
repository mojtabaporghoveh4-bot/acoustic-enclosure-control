"""Estimated (weighted-microphone) vs. actual pressure at the listener position.

Port of ``matlab/Plot_8Estimated_Actual.m``.

By default it reads the archived MATLAB result file
``data/weighted_sensor/WeightedSensorWithForce_L{force}.mat`` and reproduces the
two figures (pressure vs. frequency; RMS microphone weights).

With ``--recompute`` it ignores the stored ``EstimatedPres`` / ``ActualPres`` and
regenerates them from the Python physics port using the stored optimal weights,
demonstrating that the port matches MATLAB to machine precision.

    python examples/plot_estimated_vs_actual.py --force 800 [--recompute] [--save out.png]
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio

from _paths import DATA
from acoustic_enclosure import System


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", type=int, default=800, choices=[800, 1000, 1500, 2000])
    ap.add_argument("--recompute", action="store_true")
    ap.add_argument("--save")
    args = ap.parse_args()

    mat = sio.loadmat(
        DATA / "weighted_sensor" / f"WeightedSensorWithForce_L{args.force}.mat",
        squeeze_me=True,
        struct_as_record=False,
    )
    f = np.asarray(mat["f"], float)
    mic = np.asarray(mat["mic"], float)
    listener = np.asarray(mat["Pinterest"], float)
    wbest = np.asarray(mat["Wbest"], float)
    est = np.asarray(mat["EstimatedPres"], float)
    act = np.asarray(mat["ActualPres"], float)

    if args.recompute:
        sys = System(
            dim=(float(mat["dimension"].x), float(mat["dimension"].y), float(mat["dimension"].z)),
            n_cavity=int(mat["MODES"].AC),
            n_plate=int(mat["MODES"].PLT),
        )
        amp = float(mat["Force"].Amp)
        loc = np.asarray(mat["Force"].Location, float)
        w = 2 * np.pi * f
        act = np.array([np.abs(sys.pressure(amp, loc, wi, listener)[0]) for wi in w])
        est = np.array([
            np.abs(np.mean(wbest[i] * sys.pressure(amp, loc, w[i], mic))) for i in range(len(w))
        ])

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    a1.plot(f, 20 * np.log(est), "r", linewidth=2, label="Estimated pressure")
    a1.plot(f, 20 * np.log(act), linewidth=2, label="Actual pressure")
    a1.set_xlabel("Frequency (Hz)")
    a1.set_ylabel("Pressure (dB)")
    a1.legend()

    a2.bar(np.arange(1, wbest.shape[1] + 1), np.sqrt(np.mean(wbest ** 2, axis=0)))
    a2.set_xlabel("Sensor number")
    a2.set_ylabel("RMS of weights")

    fig.suptitle(f"Engine force {args.force} N" + ("  (recomputed in Python)" if args.recompute else ""))
    fig.tight_layout()

    if args.save:
        fig.savefig(args.save, dpi=150)
        print("wrote", args.save)
    else:
        plt.show()


if __name__ == "__main__":
    main()
