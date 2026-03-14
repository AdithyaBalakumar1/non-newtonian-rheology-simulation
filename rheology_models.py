import numpy as np

def power_law(gamma, K, n):
    return K * gamma**n

def bingham_plastic(gamma, tau_y, mu_p):
    return tau_y + mu_p * gamma

def herschel_bulkley(gamma, tau_y, K, n):
    return tau_y + K * gamma**n
