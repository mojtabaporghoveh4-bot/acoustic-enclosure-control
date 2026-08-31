# Python port — paper 01

See the [paper README](../README.md) for the full file-by-file guide and the
mapping to the original MATLAB. Quick start:

```bash
python -m pip install -r requirements.txt
python examples/plot_estimated_vs_actual.py --force 800 --recompute
pytest        # verifies the port against the archived MATLAB results
```

`acoustic_enclosure` is a small library:

- `physics.System` — modal analysis, mode shapes, coupling matrix, fully-coupled
  pressure (`CavityPressureSens.m`), region energy (`NumericalPower2Integral.m`).
- `pso.minimize` — constriction-coefficient PSO (`Best_PSO_COMPLETED.m`).
- `objectives` — the two cost functions the paper optimises.
