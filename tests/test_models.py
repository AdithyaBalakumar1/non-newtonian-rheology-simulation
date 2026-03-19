"""Tests for rheology model classes."""
import numpy as np
import pytest
from nonnewtonian.models.power_law import PowerLaw
from nonnewtonian.models.bingham import BinghamPlastic
from nonnewtonian.models.herschel_bulkley import HerschelBulkley
from nonnewtonian.flow.pipe_steady import solve_pipe_steady, validate_numerical_vs_analytical, analytical_power_law_profile


class TestPowerLaw:
    def test_shear_stress(self):
        pl = PowerLaw(K=2.0, n=1.0)
        gamma = np.array([1.0, 2.0, 3.0])
        tau = pl.shear_stress(gamma)
        expected = 2.0 * gamma ** 1.0
        np.testing.assert_allclose(tau, expected, rtol=1e-10)

    def test_newtonian_limit(self):
        """Power law with n=1 and K=mu is Newtonian (tau = mu * gamma)."""
        mu = 0.001
        pl = PowerLaw(K=mu, n=1.0)
        gamma = np.array([10.0, 100.0, 1000.0])
        tau = pl.shear_stress(gamma)
        expected = mu * gamma
        np.testing.assert_allclose(tau, expected, rtol=1e-10)

    def test_apparent_viscosity(self):
        pl = PowerLaw(K=1.0, n=0.5)
        gamma = np.array([1.0, 4.0, 9.0])
        mu = pl.apparent_viscosity(gamma)
        tau = pl.shear_stress(gamma)
        np.testing.assert_allclose(mu, tau / gamma, rtol=1e-10)

    def test_name(self):
        pl = PowerLaw(K=1.0, n=1.0)
        assert pl.name == "Power Law"


class TestBinghamPlastic:
    def test_shear_stress(self):
        bp = BinghamPlastic(tau_y=5.0, mu_p=0.5)
        gamma = np.array([1.0, 2.0, 10.0])
        tau = bp.shear_stress(gamma)
        expected = 5.0 + 0.5 * gamma
        np.testing.assert_allclose(tau, expected, rtol=1e-10)

    def test_plug_radius(self):
        bp = BinghamPlastic(tau_y=10.0, mu_p=0.5)
        r_p = bp.plug_radius(R=0.05, dpdz=-100.0)
        assert abs(r_p - 2 * 10.0 / 100.0) < 1e-10


class TestHerschelBulkley:
    def test_shear_stress(self):
        hb = HerschelBulkley(tau_y=1.0, K=0.5, n=0.7)
        gamma = np.array([1.0, 10.0, 100.0])
        tau = hb.shear_stress(gamma)
        expected = 1.0 + 0.5 * gamma ** 0.7
        np.testing.assert_allclose(tau, expected, rtol=1e-10)

    def test_reduces_to_power_law_at_zero_yield(self):
        """HB with tau_y=0 should give same stress as PowerLaw."""
        hb = HerschelBulkley(tau_y=0.0, K=0.5, n=0.7)
        pl = PowerLaw(K=0.5, n=0.7)
        gamma = np.array([1.0, 10.0, 100.0])
        np.testing.assert_allclose(hb.shear_stress(gamma), pl.shear_stress(gamma), rtol=1e-10)


class TestPipeSteady:
    def test_newtonian_poiseuille(self):
        """Power-law with n=1, K=mu should give Poiseuille profile u(0)=(-dpdz*R^2)/(4*mu)."""
        mu = 0.001
        R = 0.05
        dpdz = -100.0
        pl = PowerLaw(K=mu, n=1.0)
        results = solve_pipe_steady(pl, R=R, dpdz=dpdz, N=1000)
        u_center_numerical = results.u[0]
        u_center_poiseuille = (-dpdz * R ** 2) / (4.0 * mu)
        rel_err = abs(u_center_numerical - u_center_poiseuille) / u_center_poiseuille
        assert rel_err < 0.01, f"Newtonian limit error too large: {rel_err:.4f}"

    def test_numerical_vs_analytical_power_law(self):
        """Numerical power-law solution should match analytical within 1%."""
        val = validate_numerical_vs_analytical(R=0.05, K=0.5, n=0.7, dpdz=-100.0, N=500)
        assert val["relative_error"] < 0.01, f"Relative error too large: {val['relative_error']:.4f}"

    def test_bingham_has_plug_region(self):
        """Bingham flow should have zero velocity gradient in plug region."""
        bp = BinghamPlastic(tau_y=5.0, mu_p=0.5)
        R = 0.05
        dpdz = -100.0
        results = solve_pipe_steady(bp, R=R, dpdz=dpdz)
        assert results.r_p is not None
        assert results.r_p > 0
        r_p = results.r_p
        plug_idx = results.r < r_p * 0.9
        if plug_idx.sum() > 2:
            u_plug = results.u[plug_idx]
            variation = np.std(u_plug) / (np.mean(u_plug) + 1e-15)
            assert variation < 0.01, f"Velocity variation in plug too large: {variation:.4f}"

    def test_flow_rate_positive(self):
        """Flow rate should be positive for negative pressure gradient."""
        pl = PowerLaw(K=0.5, n=0.7)
        results = solve_pipe_steady(pl, R=0.05, dpdz=-100.0)
        assert results.Q > 0
        assert results.V_avg > 0
