import numpy as np
import matplotlib.pyplot as plt

def power_law_velocity_profile(R, K, n, dpdz):

    r = np.linspace(0, R, 200)

    # velocity profile formula for power law fluids
    v = (n/(n+1)) * ((-dpdz)/(2*K))**(1/n) * (R**((n+1)/n) - r**((n+1)/n))

    return r, v


def plot_velocity_profile():

    R = 0.05          # pipe radius (m)
    K = 0.5           # consistency index
    n = 0.7           # flow index
    dpdz = -100       # pressure gradient

    r, v = power_law_velocity_profile(R, K, n, dpdz)

    plt.figure(figsize=(7,5))

    plt.plot(r, v)

    plt.xlabel("Radius (m)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Velocity Profile for Power Law Fluid in Pipe")

    plt.grid(True)

    plt.savefig("results/pipe_velocity_profile.png")

    plt.show()
