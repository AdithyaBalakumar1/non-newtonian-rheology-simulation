"""Power-law rheology model."""
import numpy as np
from .base import RheologyModel


class PowerLaw(RheologyModel):
    """Power-law (Ostwald-de Waele) fluid model: tau = K * gamma^n."""

    def __init__(self, K: float, n: float):
        """
        Parameters
        ----------
        K : float
            Consistency index [Pa·s^n].
        n : float
            Flow behaviour index [-]. n<1 shear-thinning, n>1 shear-thickening.
        """
        self.K = K
        self.n = n

    def shear_stress(self, gamma: np.ndarray, **kwargs) -> np.ndarray:
        """Return shear stress tau = K * gamma^n."""
        return self.K * np.asarray(gamma) ** self.n

    def apparent_viscosity(self, gamma: np.ndarray, gamma_min: float = 1e-6, **kwargs) -> np.ndarray:
        """Return apparent viscosity eta = tau / gamma, bounded below by gamma_min."""
        gamma = np.asarray(gamma)
        tau = self.shear_stress(gamma)
        return tau / np.maximum(gamma, gamma_min)

    @property
    def name(self) -> str:
        return "Power Law"
