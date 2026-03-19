# Non-Newtonian Rheology Simulation

Python-based simulation of **non-Newtonian fluid rheology** including Power Law, Bingham Plastic, and 
Herschel–Bulkley models with visualization, viscosity analysis, pipe flow velocity profiles, and an 
interactive Dash simulator.

---

## Overview

Non-Newtonian fluids exhibit a nonlinear relationship between **shear stress** and **shear rate**, unlike 
Newtonian fluids where viscosity remains constant.

This project simulates the rheological behaviour of such fluids using Python and visualizes the results 
using scientific plotting tools and an interactive dashboard.

---

## Implemented Rheology Models

### Power Law Model

[
\tau = K \dot{\gamma}^{n}
]

* (K) → consistency index
* (n) → flow behavior index

Used to represent **shear-thinning** and **shear-thickening fluids**.

---
### Parameter Fitting Example

![Power Law Fit](results/powerlaw_fit.png)
### Bingham Plastic Model

[
\tau = \tau_y + \mu_p \dot{\gamma}
]

* (\tau_y) → yield stress
* (\mu_p) → plastic viscosity

Represents materials that **do not flow until a yield stress is exceeded**.

---

### Herschel–Bulkley Model

[
\tau = \tau_y + K \dot{\gamma}^{n}
]

A generalized model combining **yield stress and power-law behaviour**.

---

## Project Features

* Rheology curve simulation (shear stress vs shear rate)
* Apparent viscosity analysis
* Non-Newtonian pipe flow velocity profiles (Power Law, Bingham Plastic, Herschel-Bulkley)
* Numerical vs analytical validation for power-law pipe flow
* Multi-model parameter fitting with RMSE, R², AIC, BIC metrics
* Interactive rheology simulator (Dash dashboard) with all three models
* Markdown report generation
* Export of simulation data to CSV

---

## Project Structure

```
non-newtonian-rheology-simulation/
│
├── nonnewtonian/               # Core package
│   ├── models/                 # Rheology model classes
│   │   ├── base.py             # Abstract RheologyModel base class
│   │   ├── power_law.py        # PowerLaw model
│   │   ├── bingham.py          # BinghamPlastic model
│   │   └── herschel_bulkley.py # HerschelBulkley model
│   ├── flow/                   # Flow solvers
│   │   ├── pipe_steady.py      # Steady pipe flow solver + validation
│   │   └── dimensionless.py    # Dimensionless groups (Metzner-Reed Re)
│   ├── fitting/                # Parameter fitting
│   │   ├── datasets.py         # CSV data loader
│   │   ├── metrics.py          # RMSE, R², AIC, BIC
│   │   └── fitters.py          # Multi-model curve fitting
│   ├── viz/
│   │   └── plots.py            # Scientific plotting functions
│   └── reporting/
│       └── report.py           # Markdown report generator
│
├── scripts/
│   ├── run_rheology.py         # Main simulation script
│   ├── fit_from_csv.py         # Standalone CSV fitting tool
│   └── run_dashboard.py        # Launch Dash dashboard
│
├── tests/
│   ├── test_models.py          # Model and pipe flow tests
│   └── test_fitting.py         # Fitting tests
│
├── data/
│   └── rheology_experiment.csv
├── results/                    # Generated plots and reports
├── main.py                     # Backward-compatible entry point
├── dashboard.py                # Upgraded Dash dashboard
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```
git clone https://github.com/AdithyaBalakumar1/non-newtonian-rheology-simulation.git
cd non-newtonian-rheology-simulation
```

Create virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Running the Simulation

Run the full rheology simulation (generates plots, CSV, and a Markdown report):

```
python scripts/run_rheology.py
```

Or using the backward-compatible entry point:

```
python main.py
```

This generates:

* Rheology curves for all three models
* Apparent viscosity curves
* Steady pipe flow profiles (velocity, shear stress, apparent viscosity)
* Numerical vs analytical validation plot for power-law flow
* Model fitting results (if `data/rheology_experiment.csv` is present)
* Markdown report in `results/<run_id>/report.md`

Results are saved in the **results/** directory.

---

## Fitting Models to Experimental Data

```
python scripts/fit_from_csv.py data/rheology_experiment.csv --save results/model_fits.png
```

---

## Interactive Rheology Dashboard

Launch the simulator:

```
python scripts/run_dashboard.py
```

Or directly:

```
python dashboard.py
```

Open in browser:

```
http://127.0.0.1:8050/
```

The dashboard allows real-time adjustment of rheological parameters for all three models.

---

## Running Tests

```
pytest tests/ -v
```

---

## Applications

* Chemical engineering rheology analysis
* Computational fluid mechanics studies
* Educational demonstrations of non-Newtonian fluids
* Scientific visualization of rheological models

---

## Future Improvements

* 2D velocity field visualization
* CFD-based non-Newtonian flow solver
* Experimental data fitting
* GUI-based rheology simulator

---

## Author

Adithya Balakumar

GitHub:
https://github.com/AdithyaBalakumar1

---

## Simulation Results

### Rheology Curve
Shear stress vs shear rate for different non-Newtonian models.

![Rheology Curve](results/rheology_curve.png)

---

### Viscosity Curve
Apparent viscosity variation with shear rate.

![Viscosity Curve](results/viscosity_curve.png)

---

### Pipe Flow Velocity Profile
Velocity distribution for a power-law fluid in laminar pipe flow.

![Pipe Flow Velocity](results/pipe_velocity_profile.png)

### 2D Velocity Field Simulation

Velocity distribution inside a circular pipe for a power-law fluid.

![Velocity Field](results/velocity_field.png)
