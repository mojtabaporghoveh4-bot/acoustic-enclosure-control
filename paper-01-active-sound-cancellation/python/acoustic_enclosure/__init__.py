"""Fully-coupled plate/cavity acoustics + PSO control, Python port.

See the package README for the mapping to the original MATLAB files.
"""
from .physics import (
    System,
    cavity_modes,
    plate_modes,
    cavity_mode_shape,
    plate_mode_shape,
    coupling_term,
    region_energy,
)
from .pso import PSOOptions, PSOResult, minimize
from .objectives import TargetZone, speaker_placement_cost, sensor_weight_cost

__version__ = "0.1.0"

__all__ = [
    "System",
    "cavity_modes",
    "plate_modes",
    "cavity_mode_shape",
    "plate_mode_shape",
    "coupling_term",
    "region_energy",
    "PSOOptions",
    "PSOResult",
    "minimize",
    "TargetZone",
    "speaker_placement_cost",
    "sensor_weight_cost",
]
