#!/usr/bin/env python3
"""
Replacement for main.py: generate rheology curves, viscosity curves, pipe flow profiles,
and a Markdown report.
"""
import sys
import os
import datetime
import numpy as np
import pandas as pd

# Allow running from repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use("Agg")

from nonnewtonian.models.power_law import PowerLaw
from nonnewtonian.models.bingham import BinghamPlastic
from nonnewtonian.models.herschel_bulkley import HerschelBulkley
from nonnewtonian.flow.pipe_steady import solve_pipe_steady, validate_numerical_vs_analytical
from nonnewtonian.fitting.datasets import load_rheology_csv
from nonnewtonian.fitting.fitters import fit_all_models
from nonnewtonian.viz.plots import (
    plot_rheology_curves,
    plot_viscosity_curves,
    plot_pipe_flow_profiles,
    plot_fitting_results,
    plot_numerical_vs_analytical,
)
from nonnewtonian.reporting.report import generate_report


def main():
    print("=== Non-Newtonian Rheology Simulation ===")

    pl = PowerLaw(K=0.5, n=0.7)
    bp = BinghamPlastic(tau_y=2.0, mu_p=0.3)
    hb = HerschelBulkley(tau_y=1.0, K=0.4, n=0.6)
    models = [pl, bp, hb]

    gamma = np.logspace(-1, 3, 200)

    os.makedirs("results", exist_ok=True)

    fig1 = plot_rheology_curves(gamma, models, save_path="results/rheology_curve.png")
    print("Saved: results/rheology_curve.png")
    fig2 = plot_viscosity_curves(gamma, models, save_path="results/viscosity_curve.png")
    print("Saved: results/viscosity_curve.png")

    tau_results = {m.name: m.shear_stress(gamma) for m in models}
    df = pd.DataFrame({"shear_rate": gamma, **tau_results})
    df.to_csv("results/simulation_results.csv", index=False)
    print("Saved: results/simulation_results.csv")

    R, dpdz = 0.05, -100.0
    pipe_results = []
    plot_paths = ["results/rheology_curve.png", "results/viscosity_curve.png"]
    for model in models:
        res = solve_pipe_steady(model, R=R, dpdz=dpdz)
        pipe_results.append(res)
        safe_name = res.model_name.lower().replace(" ", "_").replace("-", "_")
        fig = plot_pipe_flow_profiles(res, save_path=f"results/pipe_{safe_name}.png")
        plot_paths.append(f"results/pipe_{safe_name}.png")
        print(f"[{res.model_name}] tau_w={res.tau_w:.3f} Pa, Q={res.Q:.4e} m³/s, V={res.V_avg:.4f} m/s", end="")
        if res.r_p is not None:
            print(f", r_p={res.r_p:.4f} m", end="")
        if res.Re_g is not None:
            print(f", Re_g={res.Re_g:.1f}", end="")
        print()

    val = validate_numerical_vs_analytical(R=R, K=0.5, n=0.7, dpdz=-100.0)
    fig_val = plot_numerical_vs_analytical(val, save_path="results/validation_powerlaw.png")
    plot_paths.append("results/validation_powerlaw.png")
    print(f"Validation L2 error: {val['l2_error']:.2e}, relative: {val['relative_error']:.2e}")

    fit_results = None
    try:
        gamma_data, tau_data = load_rheology_csv("data/rheology_experiment.csv")
        fit_results = fit_all_models(gamma_data, tau_data)
        fig_fit = plot_fitting_results(gamma_data, tau_data, fit_results, save_path="results/model_fits.png")
        plot_paths.append("results/model_fits.png")
        for key, res in fit_results.items():
            if "error" not in res:
                print(f"[{res['model']}] params={res['params']}, R²={res['r2']:.4f}, RMSE={res['rmse']:.4f}")
    except Exception as e:
        print(f"Fitting skipped: {e}")

    run_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    model_scalars = {
        m.name: {"params": str(m.__dict__)} for m in models
    }
    report_path = generate_report(
        run_id=run_id,
        model_results=model_scalars,
        pipe_flow_results=pipe_results,
        fit_results=fit_results,
        plot_paths=plot_paths,
    )
    print(f"\nReport: {report_path}")
    print("=== Done ===")


if __name__ == "__main__":
    main()
