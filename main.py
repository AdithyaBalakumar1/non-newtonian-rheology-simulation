import numpy as np
import pandas as pd

from rheology_models import power_law, bingham_plastic, herschel_bulkley
from visualization import plot_rheology, plot_viscosity
from pipe_flow import plot_velocity_profile
print("Simulation started...")

# shear rate range
gamma = np.logspace(-1,3,200)

# compute stresses
tau_power = power_law(gamma,0.5,0.7)
tau_bingham = bingham_plastic(gamma,2,0.3)
tau_hb = herschel_bulkley(gamma,1,0.4,0.6)
visc_power = tau_power / gamma
visc_bingham = tau_bingham / gamma
visc_hb = tau_hb / gamma
tau_results = {
    "Power Law": tau_power,
    "Bingham Plastic": tau_bingham,
    "Herschel Bulkley": tau_hb
}
viscosity_results = {
    "Power Law": visc_power,
    "Bingham Plastic": visc_bingham,
    "Herschel Bulkley": visc_hb
}
# plot results
plot_rheology(gamma,tau_results)
plot_viscosity(gamma, viscosity_results)
# save data
df = pd.DataFrame({
"shear_rate":gamma,
"power_law":tau_power,
"bingham":tau_bingham,
"herschel_bulkley":tau_hb
})
plot_velocity_profile()
df.to_csv("results/simulation_results.csv",index=False)

print("Simulation finished.")
