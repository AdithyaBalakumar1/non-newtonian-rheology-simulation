"""Goodness-of-fit metrics."""
import numpy as np


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root Mean Square Error."""
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def r_squared(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Coefficient of determination R²."""
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1.0 - ss_res / (ss_tot + 1e-15))


def aic(y_true: np.ndarray, y_pred: np.ndarray, k: int) -> float:
    """Akaike Information Criterion (assuming Gaussian residuals)."""
    n = len(y_true)
    rss = np.sum((y_true - y_pred) ** 2)
    sigma2 = rss / n
    log_likelihood = -n / 2.0 * np.log(2 * np.pi * sigma2) - rss / (2 * sigma2)
    return float(2 * k - 2 * log_likelihood)


def bic(y_true: np.ndarray, y_pred: np.ndarray, k: int) -> float:
    """Bayesian Information Criterion."""
    n = len(y_true)
    rss = np.sum((y_true - y_pred) ** 2)
    sigma2 = rss / n
    log_likelihood = -n / 2.0 * np.log(2 * np.pi * sigma2) - rss / (2 * sigma2)
    return float(k * np.log(n) - 2 * log_likelihood)
