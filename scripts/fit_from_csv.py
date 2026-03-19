#!/usr/bin/env python3
"""Fit rheology models to CSV data and print metrics."""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use("Agg")

from nonnewtonian.fitting.datasets import load_rheology_csv
from nonnewtonian.fitting.fitters import fit_all_models
from nonnewtonian.viz.plots import plot_fitting_results


def main():
    parser = argparse.ArgumentParser(description="Fit rheology models to CSV data.")
    parser.add_argument("csv_path", help="Path to CSV with shear_rate and shear_stress columns.")
    parser.add_argument("--save", default="results/model_fits.png", help="Path to save plot.")
    args = parser.parse_args()

    gamma, tau = load_rheology_csv(args.csv_path)
    print(f"Loaded {len(gamma)} data points from {args.csv_path}")

    results = fit_all_models(gamma, tau)
    for key, res in results.items():
        if "error" in res:
            print(f"[{key}] Error: {res['error']}")
        else:
            print(f"\n[{res['model']}]")
            for pname, pval in res["params"].items():
                print(f"  {pname} = {pval:.6f}")
            print(f"  RMSE = {res['rmse']:.6f}")
            print(f"  R²   = {res['r2']:.6f}")
            print(f"  AIC  = {res['aic']:.4f}")
            print(f"  BIC  = {res['bic']:.4f}")

    save_dir = os.path.dirname(args.save)
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
    plot_fitting_results(gamma, tau, results, save_path=args.save)
    print(f"\nPlot saved: {args.save}")


if __name__ == "__main__":
    main()
