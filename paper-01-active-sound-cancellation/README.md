# Paper 01 — Active Sound Cancellation in a Plate–Cavity Enclosure

## The problem

A thin, simply-supported aluminium plate (5 mm) forms one wall of an otherwise
rigid rectangular cavity (2.5 × 1.3 × 1.4 m — roughly a car cabin). A point
"engine" force drives the plate, the plate radiates into the cavity, and we want
to make the interior quieter. Two questions are studied:

1. **Secondary-source placement.** Where should one or two loudspeakers sit
   inside the cavity, and how strong should they be, to minimise the acoustic
   potential energy in a target zone — at each excitation frequency?
2. **Microphone-array estimation.** Real systems cannot put a microphone at the
   listener's ear. Given a fixed set of 8 microphones elsewhere in the cabin,
   what weighted combination of their signals best estimates the true pressure at
   the listener position?

Both are posed as per-frequency optimisation problems and solved with a
metaheuristic. **Particle Swarm Optimisation (PSO)** was compared against a
Genetic Algorithm, the Bees Algorithm and Grey Wolf Optimisation, and was
selected as the best trade-off of convergence and cost — it is the algorithm
carried forward in the wider project.

## The model (shared physics)

The plate and cavity are each expanded in their own modes and coupled through a
modal coupling matrix. For every frequency the coupled response is a single
linear solve. See the module docstring in
[`python/acoustic_enclosure/physics.py`](python/acoustic_enclosure/physics.py)
for the equations.

## MATLAB code (`matlab/`)

These are the original files, used as-is for the paper. Two lines were adjusted
to point at the relocated data folder (`Plot_8Estimated_Actual.m`,
`plotter_optimization_comparison.m`); those changes are commented in place.

### Modal analysis
| File | What it does |
| --- | --- |
| `cavity_freq.m` | Natural (radian) frequencies and `[n1 n2 n3]` modal indices of the rigid cavity, sorted, first *N* kept. |
| `plate_freq.m` | Same for the simply-supported plate, indices `[m1 m2]`. |
| `VNonZeros.m` | Helper: number of non-zero entries per modal-index row (sets the `√2` mode-shape normalisation). |

### Mode shapes
| File | What it does |
| --- | --- |
| `acc_mode_ne_sen.m` | Rigid-cavity acoustic mode shapes evaluated at a set of points, with the `√2^(#non-zero)` norm. |
| `plt_mdes_ne.m` | Simply-supported plate mode shapes at a point. |
| `reconstructed/acc_mode_ne.m` | **Reconstructed** (original missing). Single-point cavity mode shape used by `Accffs_opt_TwoSpkr.m`; identical in form to `acc_mode_ne_sen.m` and checked against the archived results. |

### Coupled system
| File | What it does |
| --- | --- |
| `CplFast.m` | One plate–cavity modal coupling coefficient (closed form). |
| `systemproperties.m` | Builds the `plate` and `cavity` structs (material properties, modal data) and the full coupling matrix `C`. |
| `CavityPressureSens.m` | Fully-coupled complex pressure at any point(s), given the engine force and up to two secondary sources. |
| `Accffs_opt_TwoSpkr.m` | Same solve, returning the cavity modal coefficients (used inside the placement objective). |
| `NumericalPower2Integral.m` | Volume integral of \|p\|² over a meshed sub-region — the "acoustic energy in the zone" objective. |

### Optimisation
| File | What it does |
| --- | --- |
| `Best_PSO_COMPLETED.m` | PSO with Clerc–Kennedy constriction coefficients (φ₁ = φ₂ = 2.05), velocity clamping at 10 % of range, reflecting walls. **The selected algorithm.** |
| `Kuri_Murales_Cost_PSO.m` | Wraps a cost function with a Kuri–Marroquín-style constraint penalty. |
| `reconstructed/CONS.m` | **Reconstructed** (original missing). Geometric constraint measure — 0 inside the cavity box, positive overshoot outside. Exact original penalty shape could not be recovered; the PSO bounds make it 0 in the archived runs. |

### Driver scripts
| File | What it does |
| --- | --- |
| `PSO_2Speaker_Pressure_Min.m` | Sweeps frequency, runs PSO over `[x1 y1 z1 q1 x2 y2 z2 q2]` to minimise zone energy. Saves `TwoSpeaker_output_with_Force*.mat`. |
| `PSO_2Speaker_Pressure_Min_Large.m` | Same, higher plate-mode count / larger settings. |
| `Sensor8_PSO.m` | Sweeps frequency, runs PSO over the 8 microphone weights to match the listener pressure. Saves `WeightedSensorWithForce_L*.mat`. |
| `automated_PSO_Sensor8.m` | Batch version of the above over several engine-force levels. |
| `run_in_order_all_forces.m` | Loops the sensor optimisation over the force list `[800 1000 1500 2000]` N. |

### Figure scripts
| File | Figure |
| --- | --- |
| `Plot_8Estimated_Actual.m` | Estimated (weighted-microphone) vs. actual listener pressure over frequency; RMS of the optimal weights per sensor. Reads `data/weighted_sensor/WeightedSensorWithForce_L{force}.mat`. |
| `plotter_optimization_comparison.m` | Convergence of PSO / GA / BA / GWO on a log-iteration axis. Reads `data/optimization_comparison/Data_*.xlsx`. |
| `Optimum_number_of_speakers.m` | Cumulative estimation error vs. number of secondary speakers (hard-coded study data). |

## Python port (`python/`)

```
acoustic_enclosure/
  physics.py      System, modal analysis, mode shapes, coupling, coupled pressure, region energy
  pso.py          minimize() — the constriction PSO (port of Best_PSO_COMPLETED.m)
  objectives.py   speaker_placement_cost, sensor_weight_cost, TargetZone
examples/
  plot_optimization_comparison.py   -> plotter_optimization_comparison.m
  plot_estimated_vs_actual.py       -> Plot_8Estimated_Actual.m  (add --recompute to regenerate from the port)
  run_speaker_placement_pso.py      -> PSO_2Speaker_Pressure_Min.m
  run_sensor_weight_pso.py          -> Sensor8_PSO.m
tests/
  test_against_matlab.py            -> checks the port vs. the archived .mat files
```

### Setup

```bash
cd paper-01-active-sound-cancellation/python
python -m pip install -r requirements.txt      # numpy, scipy, matplotlib, pandas, openpyxl, pytest
```

### Reproduce the figures

```bash
python examples/plot_optimization_comparison.py
python examples/plot_estimated_vs_actual.py --force 800
python examples/plot_estimated_vs_actual.py --force 2000 --recompute   # recomputed by the Python physics
```

### Re-run the optimisations (slower — genuine PSO runs)

```bash
python examples/run_sensor_weight_pso.py --force 800 --freqs 40 --iter 300 --plot
python examples/run_speaker_placement_pso.py --freqs 6 --iter 300 --plot
```

### Verify the port

```bash
cd python && pytest
```

`test_against_matlab.py` loads every `WeightedSensorWithForce_L*.mat` and checks
the cavity/plate modal frequencies, the mode indices, the coupling matrix and the
estimated/actual pressure curves against the Python port. All match to machine
precision.

## Data (`data/`)

| Path | Origin | Used by |
| --- | --- | --- |
| `optimization_comparison/Data_{PSO,GA,BA,GWO}.xlsx` | Digitised convergence traces from the algorithm comparison. | `plotter_optimization_comparison.m` |
| `optimization_comparison/Data_*.csv` | Dependency-free copies of the above. | `plot_optimization_comparison.py` |
| `weighted_sensor/WeightedSensorWithForce_L{800,1000,1500,2000}.mat` | Full workspace of a `Sensor8_PSO.m` run at each engine force. Renamed from the original `…L800 .mat` (trailing space). | `Plot_8Estimated_Actual.m`, `plot_estimated_vs_actual.py`, the tests |
| `weighted_sensor/PSOWeightedSensor_*.mat`, `P_PSOWeightedSensor_L800.mat` | Earlier 5- / 6-microphone and pressure-only runs. | reference |

## Reconstructed files

`matlab/reconstructed/` holds `acc_mode_ne.m` and `CONS.m`, which were called by
the archived scripts but were themselves missing. Each carries a header
explaining the reconstruction. `acc_mode_ne.m` is a faithful single-point form of
`acc_mode_ne_sen.m` (verified against the results); `CONS.m` is a best-effort
box-constraint measure whose exact original form is unknown but which does not
affect the archived runs.

## Citing

Cite the published paper (not this repository) for the method. This code is
released under the MIT License.
