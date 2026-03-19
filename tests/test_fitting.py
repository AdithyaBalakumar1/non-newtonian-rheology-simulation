"""Tests for parameter fitting."""
import numpy as np
import pytest
from nonnewtonian.fitting.fitters import fit_power_law, fit_bingham, fit_herschel_bulkley, fit_all_models
from nonnewtonian.fitting.metrics import rmse, r_squared


def make_power_law_data(K=0.5, n=0.7, n_points=30, noise_frac=0.02):
    rng = np.random.default_rng(42)
    gamma = np.logspace(-1, 3, n_points)
    tau = K * gamma**n * (1 + noise_frac * rng.standard_normal(n_points))
    return gamma, np.maximum(tau, 1e-6)


def make_bingham_data(tau_y=5.0, mu_p=0.3, n_points=30, noise_frac=0.02):
    rng = np.random.default_rng(42)
    gamma = np.linspace(0.1, 100.0, n_points)
    tau = tau_y + mu_p * gamma * (1 + noise_frac * rng.standard_normal(n_points))
    return gamma, np.maximum(tau, 1e-6)


class TestFitters:
    def test_power_law_fit_shape(self):
        gamma, tau = make_power_law_data()
        res = fit_power_law(gamma, tau)
        assert "params" in res
        assert "K" in res["params"] and "n" in res["params"]
        assert "rmse" in res and "r2" in res

    def test_power_law_fit_accuracy(self):
        gamma, tau = make_power_law_data(K=0.5, n=0.7)
        res = fit_power_law(gamma, tau)
        assert abs(res["params"]["K"] - 0.5) / 0.5 < 0.05
        assert abs(res["params"]["n"] - 0.7) / 0.7 < 0.05
        assert res["r2"] > 0.99

    def test_bingham_fit_shape(self):
        gamma, tau = make_bingham_data()
        res = fit_bingham(gamma, tau)
        assert "params" in res
        assert "tau_y" in res["params"] and "mu_p" in res["params"]

    def test_bingham_fit_accuracy(self):
        gamma, tau = make_bingham_data(tau_y=5.0, mu_p=0.3)
        res = fit_bingham(gamma, tau)
        assert abs(res["params"]["tau_y"] - 5.0) / 5.0 < 0.05
        assert abs(res["params"]["mu_p"] - 0.3) / 0.3 < 0.05
        assert res["r2"] > 0.99

    def test_fit_all_returns_three_models(self):
        gamma, tau = make_power_law_data()
        results = fit_all_models(gamma, tau)
        assert "power_law" in results
        assert "bingham" in results
        assert "herschel_bulkley" in results

    def test_metrics(self):
        y = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.1, 1.9, 3.05])
        r2 = r_squared(y, y_pred)
        rm = rmse(y, y_pred)
        assert 0.98 < r2 <= 1.0
        assert rm < 0.1
