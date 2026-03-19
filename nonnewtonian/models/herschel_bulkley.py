"""Herschel-Bulkley rheology model."""
import numpy as np
from .base import RheologyModel


class HerschelBulkley(RheologyModel):
    """Herschel-Bulkley model: tau = tau_y + K * gamma^n (for gamma > 0)."""

    def __init__(self, tau_y: float, K: float, n: float):
        """
        Parameters
        ----------
        tau_y : float
            Yield stress [Pa].
        K : float
            Consistency index [Pa·s^n].
        n : float
            Flow behaviour index [-].
        """
        self.tau_y = tau_y
        self.K = K
        self.n = n

    def shear_stress(self, gamma: np.ndarray, **kwargs) -> np.ndarray:
        """Return shear stress tau = tau_y + K * gamma^n."""
        gamma = np.asarray(gamma)
        return self.tau_y + self.K * gamma ** self.n

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
        return "Herschel-Bulkley"
