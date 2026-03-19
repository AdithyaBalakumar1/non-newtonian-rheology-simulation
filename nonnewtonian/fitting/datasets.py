"""Dataset loading and validation for rheology fitting."""
import numpy as np
import pandas as pd
from pathlib import Path


def load_rheology_csv(path: str) -> tuple:
    """
    Load rheology data from CSV.

    Requires columns: 'shear_rate', 'shear_stress'.
    Validates nonnegative values.

    Returns
    -------
    (gamma, tau) as numpy arrays
    """
    df = pd.read_csv(path)
    required = {"shear_rate", "shear_stress"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required}. Found: {set(df.columns)}")

    gamma = df["shear_rate"].values.astype(float)
    tau = df["shear_stress"].values.astype(float)

    if np.any(gamma < 0):
        raise ValueError("shear_rate values must be nonnegative.")
    if np.any(tau < 0):
        raise ValueError("shear_stress values must be nonnegative.")

    return gamma, tau
