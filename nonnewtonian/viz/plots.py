"""Scientific plotting for non-Newtonian rheology and pipe flow."""
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
from typing import Dict, Optional, List
from pathlib import Path

from ..models.base import RheologyModel


def plot_rheology_curves(
    gamma: np.ndarray,
    models: List[RheologyModel],
    save_path: Optional[str] = None,
    show: bool = False,
) -> plt.Figure:
    """Plot shear stress vs shear rate for multiple models."""
    fig, ax = plt.subplots(figsize=(8, 6))
    for model in models:
        tau = model.shear_stress(gamma)
        ax.loglog(gamma, tau, label=model.name, linewidth=2)
    ax.set_xlabel("Shear Rate $\\dot{\\gamma}$ (s$^{-1}$)", fontsize=12)
    ax.set_ylabel("Shear Stress $\\tau$ (Pa)", fontsize=12)
    ax.set_title("Rheology Curves: Shear Stress vs Shear Rate", fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig


def plot_viscosity_curves(
    gamma: np.ndarray,
    models: List[RheologyModel],
    gamma_min: float = 1e-3,
    save_path: Optional[str] = None,
    show: bool = False,
) -> plt.Figure:
    """Plot apparent viscosity vs shear rate for multiple models."""
    gamma_plot = np.maximum(gamma, gamma_min)
    fig, ax = plt.subplots(figsize=(8, 6))
    for model in models:
        mu_app = model.apparent_viscosity(gamma_plot, gamma_min=gamma_min)
        ax.loglog(gamma_plot, mu_app, label=model.name, linewidth=2)
    ax.set_xlabel("Shear Rate $\\dot{\\gamma}$ (s$^{-1}$)", fontsize=12)
    ax.set_ylabel("Apparent Viscosity $\\eta$ (Pa·s)", fontsize=12)
    ax.set_title("Apparent Viscosity vs Shear Rate", fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig


def plot_pipe_flow_profiles(
    results,  # PipeFlowResults
    save_path: Optional[str] = None,
    show: bool = False,
) -> plt.Figure:
    """Plot pipe flow profiles: u(r), tau(r), mu_app(r)."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].plot(results.u, results.r, 'b-', linewidth=2)
    axes[0].set_xlabel("Velocity u (m/s)", fontsize=11)
    axes[0].set_ylabel("Radial position r (m)", fontsize=11)
    axes[0].set_title(f"Velocity Profile\n{results.model_name}", fontsize=11)
    axes[0].grid(True, alpha=0.3)
    if results.r_p is not None:
        axes[0].axhline(y=results.r_p, color='r', linestyle='--',
                        label=f"Plug radius r_p={results.r_p:.4f} m")
        axes[0].legend(fontsize=9)

    axes[1].plot(results.tau, results.r, 'g-', linewidth=2)
    axes[1].set_xlabel("Shear Stress $\\tau$ (Pa)", fontsize=11)
    axes[1].set_ylabel("Radial position r (m)", fontsize=11)
    axes[1].set_title(f"Shear Stress Profile\n{results.model_name}", fontsize=11)
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(results.mu_app, results.r, 'm-', linewidth=2)
    axes[2].set_xlabel("Apparent Viscosity $\\eta$ (Pa·s)", fontsize=11)
    axes[2].set_ylabel("Radial position r (m)", fontsize=11)
    axes[2].set_title(f"Apparent Viscosity Profile\n{results.model_name}", fontsize=11)
    axes[2].grid(True, alpha=0.3)

    fig.suptitle(
        f"Steady Pipe Flow — {results.model_name} | "
        f"R={results.R} m, dp/dz={results.dpdz} Pa/m",
        fontsize=12,
    )
    fig.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig


def plot_fitting_results(
    gamma: np.ndarray,
    tau_measured: np.ndarray,
    fit_results: Dict,
    save_path: Optional[str] = None,
    show: bool = False,
) -> plt.Figure:
    """Plot measured data and fitted model curves."""
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(gamma, tau_measured, color='black', s=40, zorder=5, label="Measured data", alpha=0.8)

    gamma_plot = np.logspace(np.log10(gamma.min()), np.log10(gamma.max()), 200)

    for key, res in fit_results.items():
        if "error" in res:
            continue
        params = res["params"]
        model_name = res["model"]
        r2 = res.get("r2", float("nan"))
        rmse_val = res.get("rmse", float("nan"))

        if key == "power_law":
            tau_fit = params["K"] * gamma_plot ** params["n"]
        elif key == "bingham":
            tau_fit = params["tau_y"] + params["mu_p"] * gamma_plot
        elif key == "herschel_bulkley":
            tau_fit = params["tau_y"] + params["K"] * gamma_plot ** params["n"]
        else:
            continue

        ax.loglog(gamma_plot, tau_fit, linewidth=2,
                  label=f"{model_name} (R²={r2:.3f}, RMSE={rmse_val:.3f})")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Shear Rate $\\dot{\\gamma}$ (s$^{-1}$)", fontsize=12)
    ax.set_ylabel("Shear Stress $\\tau$ (Pa)", fontsize=12)
    ax.set_title("Model Fitting Results", fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig


def plot_numerical_vs_analytical(
    validation: Dict,
    save_path: Optional[str] = None,
    show: bool = False,
) -> plt.Figure:
    """Plot numerical vs analytical power-law velocity profiles."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    r = validation["r"]
    u_num = validation["u_numerical"]
    u_ana = validation["u_analytical"]

    axes[0].plot(u_ana, r, 'b-', linewidth=2, label="Analytical")
    axes[0].plot(u_num, r, 'r--', linewidth=2, label="Numerical")
    axes[0].set_xlabel("Velocity u (m/s)", fontsize=11)
    axes[0].set_ylabel("Radial position r (m)", fontsize=11)
    axes[0].set_title("Numerical vs Analytical Power-Law Profile", fontsize=11)
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(r, np.abs(u_num - u_ana), 'g-', linewidth=2)
    axes[1].set_xlabel("Radial position r (m)", fontsize=11)
    axes[1].set_ylabel("|Error| (m/s)", fontsize=11)
    axes[1].set_title(
        f"Absolute Error\nL2={validation['l2_error']:.2e}, rel={validation['relative_error']:.2e}",
        fontsize=11,
    )
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig
