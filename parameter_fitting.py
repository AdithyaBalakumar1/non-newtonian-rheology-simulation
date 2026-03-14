import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def power_law(gamma, K, n):
    return K * gamma**n


def fit_power_law():

    data = pd.read_csv("data/rheology_experiment.csv")

    gamma = data["shear_rate"].values
    tau = data["shear_stress"].values

    params, _ = curve_fit(power_law, gamma, tau)

    K_fit, n_fit = params

    print("Estimated Parameters:")
    print("K =", K_fit)
    print("n =", n_fit)

    gamma_fit = np.logspace(-1,3,200)
    tau_fit = power_law(gamma_fit, K_fit, n_fit)

    plt.figure(figsize=(8,6))

    plt.scatter(gamma, tau, label="Experimental Data")
    plt.loglog(gamma_fit, tau_fit, label="Fitted Power Law")

    plt.xlabel("Shear Rate (1/s)")
    plt.ylabel("Shear Stress (Pa)")
    plt.title("Power Law Model Fit")

    plt.legend()
    plt.grid(True)

    plt.savefig("results/powerlaw_fit.png")

    plt.show()
