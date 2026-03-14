import numpy as np
import matplotlib.pyplot as plt


def power_law_velocity(r, R, K, n, dpdz):

    return (n/(n+1))*((-dpdz)/(2*K))**(1/n)*(R**((n+1)/n)-r**((n+1)/n))


def plot_velocity_field():

    R = 0.05
    K = 0.5
    n = 0.7
    dpdz = -100

    # create grid
    x = np.linspace(-R, R, 200)
    y = np.linspace(-R, R, 200)

    X, Y = np.meshgrid(x, y)

    r = np.sqrt(X**2 + Y**2)

    velocity = power_law_velocity(r, R, K, n, dpdz)

    velocity[r > R] = np.nan

    plt.figure(figsize=(6,6))

    plt.contourf(X, Y, velocity, levels=50)
    plt.colorbar(label="Velocity (m/s)")

    plt.title("2D Velocity Field in Pipe (Power-Law Fluid)")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")

    plt.gca().set_aspect('equal')

    plt.savefig("results/velocity_field.png")

    plt.show()
