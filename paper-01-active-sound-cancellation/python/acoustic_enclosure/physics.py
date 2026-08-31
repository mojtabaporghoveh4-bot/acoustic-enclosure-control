"""Fully-coupled plate / rigid-cavity acoustic model.

Python port of the MATLAB routines used in the "active sound cancellation in an
acoustic enclosure" work:

    cavity_freq.m        -> cavity_modes
    plate_freq.m         -> plate_modes
    acc_mode_ne_sen.m    -> cavity_mode_shape
    plt_mdes_ne.m        -> plate_mode_shape
    VNonZeros.m          -> (np.count_nonzero)
    CplFast.m            -> coupling_term
    systemproperties.m   -> System
    CavityPressureSens.m -> System.pressure
    Accffs_opt_TwoSpkr.m -> System.cavity_coefficients
    NumericalPower2Integral.m -> region_energy

The port reproduces the modal frequencies, mode indices, coupling matrix and
fully-coupled pressure stored in the archived ``WeightedSensorWithForce_*.mat``
result files to machine precision (see ``tests/test_against_matlab.py``).

Model
-----
A thin simply-supported aluminium plate forms one wall of an otherwise
rigid-walled rectangular cavity.  The plate is driven by a point force
(the "engine"); up to two secondary monopole sources inside the cavity are the
control actuators.  Plate and cavity modes are coupled through the matrix ``C``
and the response is solved as one linear system per frequency.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

__all__ = [
    "cavity_modes",
    "plate_modes",
    "cavity_mode_shape",
    "plate_mode_shape",
    "coupling_term",
    "region_energy",
    "System",
]


def _first_n_unique(w, idx, n, decimals=6):
    """Take the first ``n`` entries with distinct frequency (already sorted)."""
    keep_w, keep_i, seen = [], [], set()
    for wi, ii in zip(w, idx):
        key = round(float(wi), decimals)
        if key in seen:
            continue
        seen.add(key)
        keep_w.append(wi)
        keep_i.append(ii)
        if len(keep_w) == n:
            break
    return np.asarray(keep_w, float), np.asarray(keep_i, int)


def cavity_modes(n_modes, Lx, Ly, Lz, sound_speed=340.0):
    """Radian eigenfrequencies and ``[n1 n2 n3]`` indices of a rigid cavity.

    Port of ``cavity_freq.m``.  Ties (e.g. permuted indices with equal
    frequency) are broken exactly as MATLAB's column-major ``find`` would:
    smallest ``n3``, then ``n1``, then ``n2``.
    """
    M = n_modes
    idx = np.array(
        [(n1, n2, n3)
         for n3 in range(M + 1)
         for n1 in range(M + 1)
         for n2 in range(M + 1)],
        dtype=float,
    )
    w = np.pi * sound_speed * np.sqrt(
        (idx[:, 0] / Lx) ** 2 + (idx[:, 1] / Ly) ** 2 + (idx[:, 2] / Lz) ** 2
    )
    order = np.lexsort((idx[:, 1], idx[:, 0], idx[:, 2], np.round(w, 9)))
    return _first_n_unique(w[order], idx[order], M)


def plate_modes(n_modes, Lx, Ly, bending, thickness, density):
    """Radian eigenfrequencies and ``[m1 m2]`` indices of a simply-supported plate.

    Port of ``plate_freq.m`` (mode indices are 1-based).
    """
    M = n_modes
    idx = np.array(
        [(m1, m2) for m1 in range(1, M + 1) for m2 in range(1, M + 1)],
        dtype=float,
    )
    w = np.sqrt(bending / (thickness * density)) * (
        (idx[:, 0] * np.pi / Lx) ** 2 + (idx[:, 1] * np.pi / Ly) ** 2
    )
    order = np.lexsort((idx[:, 1], idx[:, 0], np.round(w, 9)))
    return _first_n_unique(w[order], idx[order], M)


def cavity_mode_shape(points, dim, idx):
    """Rigid-cavity acoustic mode shapes at one or more points.

    Port of ``acc_mode_ne_sen.m`` (and the reconstructed ``acc_mode_ne.m``).

    Parameters
    ----------
    points : (P, 3) array-like of coordinates in metres.
    dim    : (Lx, Ly, Lz) cavity dimensions.
    idx    : (K, 3) integer cavity mode indices.

    Returns
    -------
    (K, P) array – the ``sqrt(2)**(#non-zero indices)`` normalisation is applied.
    """
    pts = np.atleast_2d(np.asarray(points, float))
    dim = np.asarray(dim, float)
    idx = np.atleast_2d(np.asarray(idx))
    norm = np.sqrt(2.0) ** np.count_nonzero(idx, axis=1)
    kx = np.pi * idx[:, 0] / dim[0]
    ky = np.pi * idx[:, 1] / dim[1]
    kz = np.pi * idx[:, 2] / dim[2]
    return (
        norm[:, None]
        * np.cos(np.outer(kx, pts[:, 0]))
        * np.cos(np.outer(ky, pts[:, 1]))
        * np.cos(np.outer(kz, pts[:, 2]))
    )


def plate_mode_shape(x, y, Lx, Ly, idx):
    """Simply-supported plate mode shapes at a point. Port of ``plt_mdes_ne.m``."""
    idx = np.atleast_2d(np.asarray(idx, float))
    return 2.0 * np.sin(x * np.pi * idx[:, 0] / Lx) * np.sin(y * np.pi * idx[:, 1] / Ly)


def coupling_term(plate_idx, cavity_idx, plate_area):
    """Single plate/cavity modal coupling coefficient. Port of ``CplFast.m``."""
    n1, n2, n3 = cavity_idx
    m1, m2 = plate_idx
    er = np.sqrt(2.0) ** np.count_nonzero(cavity_idx)
    s = 2.0 * plate_area * er * (-1.0) ** n3
    if n1 != m1 and n2 != m2:
        return (
            s
            * (m1 * m2 * ((-1.0) ** (n1 + m1) - 1) * ((-1.0) ** (n2 + m2) - 1))
            / (np.pi ** 2 * (n1 ** 2 - m1 ** 2) * (n2 ** 2 - m2 ** 2))
        )
    return 0.0


def region_energy(coeffs, xmesh, ymesh, zmesh, dim, cavity_idx, dv):
    """Volume integral of |p|^2 over a meshed sub-region. Port of ``NumericalPower2Integral.m``.

    ``coeffs`` are the cavity modal coefficients returned by
    :meth:`System.cavity_coefficients`.
    """
    dim = np.asarray(dim, float)
    idx = np.atleast_2d(np.asarray(cavity_idx))
    norm = np.sqrt(2.0) ** np.count_nonzero(idx, axis=1)
    p = np.zeros(xmesh.shape, dtype=complex)
    for a, nrm, (n1, n2, n3) in zip(coeffs, norm, idx):
        p += a * nrm * (
            np.cos(xmesh * np.pi * n1 / dim[0])
            * np.cos(ymesh * np.pi * n2 / dim[1])
            * np.cos(zmesh * np.pi * n3 / dim[2])
        )
    return dv * np.sum(np.abs(p) ** 2)


@dataclass
class System:
    """Fully-coupled plate + rigid-cavity system. Port of ``systemproperties.m``.

    Defaults reproduce the aluminium plate used throughout the archived runs
    (2.5 x 1.3 x 1.4 m cabin, 5 mm plate).
    """

    dim: tuple = (2.5, 1.3, 1.4)
    n_cavity: int = 70
    n_plate: int = 50

    plate_density: float = 2770.0
    plate_poisson: float = 0.33
    plate_damping: float = 0.01
    plate_thickness: float = 5e-3
    plate_young: float = 71e9

    cavity_density: float = 1.21
    sound_speed: float = 340.0
    cavity_damping: float = 0.01
    cavity_time_constant: float = 0.2

    plate_bending: float = field(init=False)
    plate_area: float = field(init=False)
    cavity_volume: float = field(init=False)
    plate_w: np.ndarray = field(init=False, repr=False)
    plate_idx: np.ndarray = field(init=False, repr=False)
    cavity_w: np.ndarray = field(init=False, repr=False)
    cavity_idx: np.ndarray = field(init=False, repr=False)
    C: np.ndarray = field(init=False, repr=False)

    def __post_init__(self):
        Lx, Ly, Lz = self.dim
        self.plate_area = Lx * Ly
        self.cavity_volume = Lx * Ly * Lz
        self.plate_bending = (
            self.plate_young * self.plate_thickness ** 3
        ) / (12.0 * (1.0 - self.plate_poisson ** 2))

        self.plate_w, self.plate_idx = plate_modes(
            self.n_plate, Lx, Ly, self.plate_bending, self.plate_thickness, self.plate_density
        )
        self.cavity_w, self.cavity_idx = cavity_modes(
            self.n_cavity, Lx, Ly, Lz, self.sound_speed
        )

        C = np.zeros((self.n_cavity, self.n_plate))
        for j in range(self.n_cavity):
            for i in range(self.n_plate):
                C[j, i] = coupling_term(self.plate_idx[i], self.cavity_idx[j], self.plate_area)
        self.C = C

    # ------------------------------------------------------------------ solve

    def cavity_coefficients(self, force_amp, force_loc, omega, sources=None):
        """Cavity modal coefficients ``a`` at radian frequency ``omega``.

        Port of the shared core of ``CavityPressureSens.m`` /
        ``Accffs_opt_TwoSpkr.m``.

        ``sources`` : optional length-8 vector ``[x1 y1 z1 q1  x2 y2 z2 q2]``
        describing up to two secondary monopoles (positions in metres, ``q`` the
        volume-velocity amplitude). ``None`` -> primary force only.
        """
        Lx, Ly, Lz = self.dim
        g = force_amp * plate_mode_shape(force_loc[0], force_loc[1], Lx, Ly, self.plate_idx)
        B = 1j * omega / (
            self.plate_w ** 2 - omega ** 2 + 2j * self.plate_damping * omega * self.plate_w
        )

        if sources is None:
            q = np.zeros(self.n_cavity, dtype=complex)
        else:
            s = np.asarray(sources, float)
            q = (
                s[3] * cavity_mode_shape(s[0:3], self.dim, self.cavity_idx)[:, 0]
                + s[7] * cavity_mode_shape(s[4:7], self.dim, self.cavity_idx)[:, 0]
            )

        A = (1j * omega / (
            self.cavity_w ** 2 - omega ** 2 + 2j * self.cavity_damping * omega * self.cavity_w
        )).astype(complex)
        A[0] = 1.0 / (1.0 / self.cavity_time_constant + 1j * omega)  # rigid-body mode

        Za = (self.cavity_density * self.sound_speed ** 2 / self.cavity_volume) * np.diag(A)
        Ys = np.diag(B / (self.plate_density * self.plate_thickness * self.plate_area))

        lhs = np.eye(self.n_cavity) + Za @ self.C @ Ys @ self.C.T
        rhs = Za @ (q + self.C @ Ys @ g)
        return np.linalg.solve(lhs, rhs)

    def pressure(self, force_amp, force_loc, omega, points, sources=None):
        """Complex acoustic pressure at ``points`` (shape ``(P,)``).

        Port of ``CavityPressureSens.m``.
        """
        a = self.cavity_coefficients(force_amp, force_loc, omega, sources)
        shp = cavity_mode_shape(points, self.dim, self.cavity_idx)
        return a @ shp
