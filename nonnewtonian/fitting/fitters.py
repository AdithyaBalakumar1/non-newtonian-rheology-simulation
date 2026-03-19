"""Multi-model parameter fitters."""
import numpy as np
from scipy.optimize import curve_fit
from typing import Dict, Any
from .metrics import rmse, r_squared, aic, bic


def _power_law_func(gamma, K, n):
    return K * gamma ** n


def _bingham_func(gamma, tau_y, mu_p):
    return tau_y + mu_p * gamma


def _herschel_bulkley_func(gamma, tau_y, K, n):
    return tau_y + K * gamma ** n


def fit_power_law(gamma: np.ndarray, tau: np.ndarray) -> Dict[str, Any]:
    """Fit power-law model to data. Returns params and metrics."""
    params, _ = curve_fit(_power_law_func, gamma, tau, p0=[1.0, 0.5], maxfev=10000)
    K_fit, n_fit = params
    tau_pred = _power_law_func(gamma, K_fit, n_fit)
    return {
        "model": "Power Law",
        "params": {"K": K_fit, "n": n_fit},
        "rmse": rmse(tau, tau_pred),
        "r2": r_squared(tau, tau_pred),
        "aic": aic(tau, tau_pred, k=2),
        "bic": bic(tau, tau_pred, k=2),
        "tau_pred": tau_pred,
    }


def fit_bingham(gamma: np.ndarray, tau: np.ndarray) -> Dict[str, Any]:
    """Fit Bingham plastic model to data. Returns params and metrics."""
    params, _ = curve_fit(_bingham_func, gamma, tau, p0=[1.0, 0.1], bounds=(0, np.inf), maxfev=10000)
    tau_y_fit, mu_p_fit = params
    tau_pred = _bingham_func(gamma, tau_y_fit, mu_p_fit)
    return {
        "model": "Bingham Plastic",
        "params": {"tau_y": tau_y_fit, "mu_p": mu_p_fit},
        "rmse": rmse(tau, tau_pred),
        "r2": r_squared(tau, tau_pred),
        "aic": aic(tau, tau_pred, k=2),
        "bic": bic(tau, tau_pred, k=2),
        "tau_pred": tau_pred,
    }


def fit_herschel_bulkley(gamma: np.ndarray, tau: np.ndarray) -> Dict[str, Any]:
    """Fit Herschel-Bulkley model to data. Returns params and metrics."""
    params, _ = curve_fit(
        _herschel_bulkley_func, gamma, tau,
        p0=[1.0, 1.0, 0.5],
        bounds=([0, 0, 0.01], [np.inf, np.inf, 2.0]),
        maxfev=20000,
    )
    tau_y_fit, K_fit, n_fit = params
    tau_pred = _herschel_bulkley_func(gamma, tau_y_fit, K_fit, n_fit)
    return {
        "model": "Herschel-Bulkley",
        "params": {"tau_y": tau_y_fit, "K": K_fit, "n": n_fit},
        "rmse": rmse(tau, tau_pred),
        "r2": r_squared(tau, tau_pred),
        "aic": aic(tau, tau_pred, k=3),
        "bic": bic(tau, tau_pred, k=3),
        "tau_pred": tau_pred,
    }


def fit_all_models(gamma: np.ndarray, tau: np.ndarray) -> Dict[str, Dict]:
    """Fit all three models to data and return results dict."""
    results = {}
    for name, func in [
        ("power_law", fit_power_law),
        ("bingham", fit_bingham),
        ("herschel_bulkley", fit_herschel_bulkley),
    ]:
        try:
            results[name] = func(gamma, tau)
        except Exception as e:
            results[name] = {"error": str(e)}
    return results
