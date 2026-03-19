"""Bingham plastic rheology model."""
import numpy as np
from .base import RheologyModel


class BinghamPlastic(RheologyModel):
    """Bingham plastic model: tau = tau_y + mu_p * gamma (for gamma > 0)."""

    def __init__(self, tau_y: float, mu_p: float):
        """
        Parameters
        ----------
        tau_y : float
            Yield stress [Pa].
        mu_p : float
            Plastic viscosity [Pa·s].
        """
        self.tau_y = tau_y
        self.mu_p = mu_p

    def shear_stress(self, gamma: np.ndarray, **kwargs) -> np.ndarray:
        """Return shear stress tau = tau_y + mu_p * gamma (only for gamma > 0; no flow below yield)."""
        gamma = np.asarray(gamma)
        return self.tau_y + self.mu_p * gamma

    def apparent_viscosity(self, gamma: np.ndarray, gamma_min: float = 1e-6, **kwargs) -> np.ndarray:
        """Return apparent viscosity eta = tau / gamma, bounded below by gamma_min."""
        gamma = np.asarray(gamma)
        tau = self.shear_stress(gamma)
        return tau / np.maximum(gamma, gamma_min)

    def plug_radius(self, R: float, dpdz: float) -> float:
        """
        Compute plug radius for pipe flow.

        r_p = 2 * tau_y / |dp/dz|

        Parameters
        ----------
        R : float
            Pipe radius [m].
        dpdz : float
            Pressure gradient [Pa/m].

        Returns
        -------
        float
            Plug radius [m], capped at R.
        """
        if abs(dpdz) == 0:
            return float('inf')
        return 2.0 * self.tau_y / abs(dpdz)

    @property
    def name(self) -> str:
        return "Bingham Plastic"
