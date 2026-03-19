"""Steady pipe flow solver for non-Newtonian fluids."""
from dataclasses import dataclass
import numpy as np
from typing import Optional

from ..models.base import RheologyModel
from ..models.power_law import PowerLaw
from ..models.bingham import BinghamPlastic
from ..models.herschel_bulkley import HerschelBulkley


@dataclass
class PipeFlowResults:
    """Results from steady pipe flow simulation."""

    r: np.ndarray
    u: np.ndarray
    tau: np.ndarray
    gamma_dot: np.ndarray
    mu_app: np.ndarray
    tau_w: float
    Q: float
    V_avg: float
    r_p: Optional[float]  # plug radius (None if no yield stress)
    Re_g: Optional[float]  # generalized Re (for power-law)
    model_name: str
    R: float
    dpdz: float


def analytical_power_law_profile(R: float, K: float, n: float, dpdz: float, N: int = 200):
    """
    Analytical velocity profile for power-law fluid in pipe.

    Based on momentum balance: tau(r) = -r/2 * dp/dz
    Velocity: u(r) = n/(n+1) * ((-dpdz)/(2K))^(1/n) * (R^((n+1)/n) - r^((n+1)/n))
    """
    r = np.linspace(0, R, N)
    v = (n / (n + 1)) * ((-dpdz) / (2 * K)) ** (1 / n) * (R ** ((n + 1) / n) - r ** ((n + 1) / n))
    return r, v


def solve_pipe_steady(model: RheologyModel, R: float, dpdz: float, N: int = 500) -> PipeFlowResults:
    """
    Numerically solve steady, fully developed laminar pipe flow for any model.

    Physics:
    - Shear stress from momentum balance: tau(r) = |dpdz| * r / 2
    - Yield-stress models: plug region for r < r_p where tau < tau_y
    - Velocity from integrating du/dr = -gamma_dot(r), with u(R)=0

    Parameters
    ----------
    model : RheologyModel
        The rheology model instance.
    R : float
        Pipe radius [m].
    dpdz : float
        Pressure gradient dp/dz [Pa/m] (negative for flow in +z direction).
    N : int
        Number of radial grid points.

    Returns
    -------
    PipeFlowResults
    """
    tau_w = abs(dpdz) * R / 2.0
    r = np.linspace(0, R, N)
    tau = abs(dpdz) * r / 2.0

    gamma_min = 1e-10

    # Determine plug radius for yield-stress models
    r_p = None
    if isinstance(model, (BinghamPlastic, HerschelBulkley)):
        tau_y = model.tau_y
        r_p = 2.0 * tau_y / abs(dpdz) if abs(dpdz) > 0 else R
        r_p = min(r_p, R)

    # Compute shear rate from constitutive inversion
    gamma_dot = np.zeros(N)
    if isinstance(model, PowerLaw):
        with np.errstate(divide='ignore', invalid='ignore'):
            gamma_dot = np.where(tau > 0, (tau / model.K) ** (1.0 / model.n), 0.0)
    elif isinstance(model, BinghamPlastic):
        gamma_dot = np.where(tau > model.tau_y, (tau - model.tau_y) / model.mu_p, 0.0)
    elif isinstance(model, HerschelBulkley):
        with np.errstate(divide='ignore', invalid='ignore'):
            excess = np.maximum(tau - model.tau_y, 0.0)
            gamma_dot = np.where(tau > model.tau_y, (excess / model.K) ** (1.0 / model.n), 0.0)
    else:
        raise ValueError(f"Unsupported model type: {type(model)}")

    # Compute apparent viscosity
    with np.errstate(divide='ignore', invalid='ignore'):
        mu_app = np.where(gamma_dot > gamma_min, tau / gamma_dot, tau / gamma_min)

    # Integrate velocity profile: u(r) = integral from r to R of gamma_dot(r') dr'
    # Using cumulative trapezoidal integration from R to r
    u = np.zeros(N)
    for i in range(N - 2, -1, -1):
        u[i] = u[i + 1] + 0.5 * (gamma_dot[i] + gamma_dot[i + 1]) * (r[i + 1] - r[i])

    # Volumetric flow rate Q = 2*pi * integral_0^R r*u(r) dr
    Q = 2.0 * np.pi * np.trapezoid(r * u, r)

    # Average velocity V = Q / (pi * R^2)
    V_avg = Q / (np.pi * R ** 2)

    # Generalized Reynolds number for power-law (Metzner-Reed)
    Re_g = None
    if isinstance(model, PowerLaw):
        n = model.n
        K = model.K
        rho = 1000.0  # default water density
        D = 2.0 * R
        if V_avg > 0:
            factor = 8 ** (n - 1) * ((3 * n + 1) / (4 * n)) ** n
            Re_g = rho * V_avg ** (2 - n) * D ** n / (K * factor)

    return PipeFlowResults(
        r=r,
        u=u,
        tau=tau,
        gamma_dot=gamma_dot,
        mu_app=mu_app,
        tau_w=tau_w,
        Q=Q,
        V_avg=V_avg,
        r_p=r_p,
        Re_g=Re_g,
        model_name=model.name,
        R=R,
        dpdz=dpdz,
    )


def validate_numerical_vs_analytical(R: float, K: float, n: float, dpdz: float, N: int = 500):
    """
    Compare numerical solver to analytical power-law solution.

    Returns
    -------
    dict with keys: 'l2_error', 'relative_error', 'max_error'
    """
    model = PowerLaw(K=K, n=n)
    results = solve_pipe_steady(model, R, dpdz, N=N)
    r_num = results.r
    u_num = results.u

    _, u_ana = analytical_power_law_profile(R, K, n, dpdz, N=len(r_num))

    diff = u_num - u_ana
    l2 = np.sqrt(np.mean(diff ** 2))
    rel = l2 / (np.sqrt(np.mean(u_ana ** 2)) + 1e-15)
    max_err = np.max(np.abs(diff))

    return {
        "l2_error": l2,
        "relative_error": rel,
        "max_error": max_err,
        "r": r_num,
        "u_numerical": u_num,
        "u_analytical": u_ana,
    }
