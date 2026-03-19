"""Abstract base class for rheology models."""
from abc import ABC, abstractmethod
import numpy as np


class RheologyModel(ABC):
    """Abstract base class for non-Newtonian rheology models."""

    @abstractmethod
    def shear_stress(self, gamma: np.ndarray, **kwargs) -> np.ndarray:
        """
        Compute shear stress from shear rate.

        Parameters
        ----------
        gamma : np.ndarray
            Shear rate array [s^-1].

        Returns
        -------
        np.ndarray
            Shear stress [Pa].
        """

    @abstractmethod
    def apparent_viscosity(self, gamma: np.ndarray, **kwargs) -> np.ndarray:
        """
        Compute apparent viscosity from shear rate.

        Parameters
        ----------
        gamma : np.ndarray
            Shear rate array [s^-1].

        Returns
        -------
        np.ndarray
            Apparent viscosity [Pa·s].
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable model name."""
