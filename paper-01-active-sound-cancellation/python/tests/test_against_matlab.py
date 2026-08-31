"""Verify the Python port against the archived MATLAB result files.

Every ``WeightedSensorWithForce_L*.mat`` file stores the full MATLAB workspace of
a ``Sensor8_PSO.m`` run: the cavity/plate modal data, the coupling matrix ``C``,
and the estimated/actual pressure curves.  We rebuild those from the Python port
and require a machine-precision match.

    cd python && pytest
"""
from pathlib import Path

import numpy as np
import pytest
import scipy.io as sio

from acoustic_enclosure import System

DATA = Path(__file__).resolve().parents[2] / "data" / "weighted_sensor"
MAT_FILES = sorted(DATA.glob("WeightedSensorWithForce_L*.mat"))


@pytest.fixture(scope="module", params=MAT_FILES, ids=lambda p: p.stem)
def case(request):
    mat = sio.loadmat(request.param, squeeze_me=True, struct_as_record=False)
    sys = System(
        dim=(float(mat["dimension"].x), float(mat["dimension"].y), float(mat["dimension"].z)),
        n_cavity=int(mat["MODES"].AC),
        n_plate=int(mat["MODES"].PLT),
    )
    return mat, sys


def test_modal_frequencies(case):
    mat, sys = case
    assert np.allclose(sys.cavity_w, np.asarray(mat["cavity"].radfreq, float), atol=1e-6)
    assert np.allclose(sys.plate_w, np.asarray(mat["plate"].radfreq, float), rtol=1e-12)


def test_mode_indices(case):
    mat, sys = case
    assert np.array_equal(sys.cavity_idx, np.asarray(mat["cavity"].ModeIndex, int))
    assert np.array_equal(sys.plate_idx, np.asarray(mat["plate"].ModeIndex, int))


def test_coupling_matrix(case):
    mat, sys = case
    assert np.allclose(sys.C, np.asarray(mat["C"], float), atol=1e-12)


def test_actual_pressure_curve(case):
    mat, sys = case
    f = np.asarray(mat["f"], float)
    amp = float(mat["Force"].Amp)
    loc = np.asarray(mat["Force"].Location, float)
    listener = np.asarray(mat["Pinterest"], float)
    got = np.array([np.abs(sys.pressure(amp, loc, 2 * np.pi * fi, listener)[0]) for fi in f])
    assert np.allclose(got, np.asarray(mat["ActualPres"], float), rtol=1e-10)


def test_estimated_pressure_curve(case):
    mat, sys = case
    f = np.asarray(mat["f"], float)
    amp = float(mat["Force"].Amp)
    loc = np.asarray(mat["Force"].Location, float)
    mic = np.asarray(mat["mic"], float)
    wbest = np.asarray(mat["Wbest"], float)
    got = np.array([
        np.abs(np.mean(wbest[i] * sys.pressure(amp, loc, 2 * np.pi * f[i], mic)))
        for i in range(len(f))
    ])
    assert np.allclose(got, np.asarray(mat["EstimatedPres"], float), rtol=1e-9)
