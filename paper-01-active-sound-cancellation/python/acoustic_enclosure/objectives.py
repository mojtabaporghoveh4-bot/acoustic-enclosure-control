"""Cost functions optimised in the paper.

* :func:`speaker_placement_cost` – acoustic potential energy in a target zone as
  a function of two secondary-source positions/strengths
  (``PSO_2Speaker_Pressure_Min.m``).
* :func:`sensor_weight_cost` – mismatch between a weighted microphone estimate
  and the true pressure at the listener position (``Sensor8_PSO.m``).
"""
from __future__ import annotations

import numpy as np

from .physics import System, cavity_mode_shape, region_energy

__all__ = ["TargetZone", "speaker_placement_cost", "sensor_weight_cost"]


class TargetZone:
    """Meshed rectangular sub-region used for the |p|^2 volume integral.

    ``nx, ny, nz`` default to the values in ``NumericalPower2Integral.m``.  Call
    :meth:`prepare` once with the :class:`~acoustic_enclosure.System` to cache the
    modal basis on the mesh – then each :func:`speaker_placement_cost` evaluation
    is a single matrix product instead of re-evaluating 3-D cosines.
    """

    def __init__(self, x_range, y_range, z_range, nx=120, ny=80, nz=60):
        xs = np.linspace(*x_range, nx)
        ys = np.linspace(*y_range, ny)
        zs = np.linspace(*z_range, nz)
        self.xmesh, self.ymesh, self.zmesh = np.meshgrid(xs, ys, zs, indexing="xy")
        self.dv = (xs[1] - xs[0]) * (ys[1] - ys[0]) * (zs[1] - zs[0])
        self._basis = None          # (n_cavity, n_points)
        self._basis_key = None

    @classmethod
    def default(cls, dim, **kw):
        Lx, Ly, Lz = dim
        return cls((Lx / 8, Lx / 6), (Ly / 8, Ly / 3), (Lz / 8, Lz / 6), **kw)

    def prepare(self, sys: System):
        pts = np.column_stack([self.xmesh.ravel(), self.ymesh.ravel(), self.zmesh.ravel()])
        self._basis = cavity_mode_shape(pts, sys.dim, sys.cavity_idx)
        self._basis_key = id(sys)
        return self

    def energy(self, coeffs, sys: System):
        if self._basis is None or self._basis_key != id(sys):
            self.prepare(sys)
        return self.dv * np.sum(np.abs(coeffs @ self._basis) ** 2)


def speaker_placement_cost(sources, sys: System, force_amp, force_loc, omega, zone: TargetZone):
    """|p|^2 integrated over ``zone`` for a length-8 ``sources`` vector
    ``[x1 y1 z1 q1  x2 y2 z2 q2]``."""
    a = sys.cavity_coefficients(force_amp, force_loc, omega, sources=sources)
    return zone.energy(a, sys)


def sensor_weight_cost(weights, sys: System, force_amp, force_loc, omega, mics, listener):
    """|mean(w * p_mics) - p_listener| at a single frequency."""
    p_mics = sys.pressure(force_amp, force_loc, omega, mics)
    p_listener = sys.pressure(force_amp, force_loc, omega, np.atleast_2d(listener))[0]
    return float(np.abs(np.mean(np.asarray(weights) * p_mics) - p_listener))


# kept for the docstring cross-reference / direct use
_ = region_energy
