import matplotlib.pyplot as plt


def plot_rheology(gamma, tau_results):

    plt.figure(figsize=(8,6))

    for label, tau in tau_results.items():
        plt.loglog(gamma, tau, label=label)

    plt.xlabel("Shear Rate (1/s)")
    plt.ylabel("Shear Stress (Pa)")
    plt.title("Non-Newtonian Fluid Rheology")

    plt.legend()
    plt.grid(True)

    plt.savefig("results/rheology_curve.png")

    plt.show()


def plot_viscosity(gamma, viscosity_results):

    plt.figure(figsize=(8,6))

    for label, mu in viscosity_results.items():
        plt.loglog(gamma, mu, label=label)

    plt.xlabel("Shear Rate (1/s)")
    plt.ylabel("Apparent Viscosity (Pa.s)")
    plt.title("Viscosity vs Shear Rate")

    plt.legend()
    plt.grid(True)

    plt.savefig("results/viscosity_curve.png")

    plt.show()
