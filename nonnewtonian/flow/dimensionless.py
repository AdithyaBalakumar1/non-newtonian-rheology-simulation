"""Dimensionless groups for non-Newtonian pipe flow."""
import numpy as np
from typing import Optional


def metzner_reed_reynolds(rho: float, V: float, D: float, K: float, n: float) -> float:
    """
    Metzner-Reed generalized Reynolds number for power-law fluids in pipe flow.

    Re_MR = rho * V^(2-n) * D^n / (K * 8^(n-1) * ((3n+1)/(4n))^n)
    """
    factor = 8 ** (n - 1) * ((3 * n + 1) / (4 * n)) ** n
    return rho * V ** (2 - n) * D ** n / (K * factor)


def flow_regime_note(Re: float) -> str:
    """Return a regime classification note based on Re."""
    if Re < 2100:
        return f"Re = {Re:.1f}: Laminar flow (Re < 2100)"
    elif Re < 4000:
        return f"Re = {Re:.1f}: Transitional flow (2100 < Re < 4000)"
    else:
        return f"Re = {Re:.1f}: Turbulent flow (Re > 4000)"
