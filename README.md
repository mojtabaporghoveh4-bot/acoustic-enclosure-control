# Acoustic Enclosure Control

Modelling and optimisation code for a series of papers on **noise control inside
a flexible-walled acoustic enclosure** (a car-cabin-sized cavity with one thin
vibrating plate as a wall). Each paper lives in its own top-level folder with the
original MATLAB, a Python port, the data needed to reproduce its figures, and a
dedicated README.

| Folder | Paper | Contents |
| --- | --- | --- |
| [`paper-01-active-sound-cancellation/`](paper-01-active-sound-cancellation/) | Active sound cancellation in a plate–cavity enclosure (secondary-source placement and microphone-array estimation, optimised with PSO/GA/BA/GWO). | MATLAB + validated Python port + data |
| _more to come_ | | |

## Repository layout

```
paper-XX-name/
├── matlab/     original MATLAB, as used for the paper (+ a `reconstructed/` folder
│               for any helper that was missing from the archive)
├── python/     acoustic_enclosure/  – library port
│               examples/            – runnable scripts that reproduce the figures
│               tests/               – checks the port against archived MATLAB output
└── data/       inputs / archived results required by the scripts
```

## Status of the port

The Python port of paper 01 reproduces the archived MATLAB results (modal
frequencies, mode indices, coupling matrix, and the fully-coupled pressure
curves) **to machine precision** — see `paper-01-.../python/tests/`.

## Provenance

The physics engine used in paper 01 was written during the sensor-placement study
(internal name "Sarbazi sensor article"); contributions from co-authors are
acknowledged in each paper folder. Code is released under the MIT License (see
[`LICENSE`](LICENSE)). The papers themselves are not redistributed here — cite
the published versions.

## Key reference

The coupled plate–cavity model used throughout is the analytical framework of:

> Porghoveh, M., Heidari Shirazi, K., & Yildizdag, M. E. (2021). *A fast
> analytical framework to identify acoustic field properties of rectangular
> enclosures with a vibrating plate.* Applied Acoustics, 182, 108185.
> https://doi.org/10.1016/j.apacoust.2021.108185

## Author

Mojtaba Porghoveh · <mojtabaporghoveh4@gmail.com>
