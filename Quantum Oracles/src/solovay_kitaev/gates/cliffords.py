import numpy as np


inv_sqrt_2 = 1 / (2 ** 0.5)

hadamard = inv_sqrt_2 * np.array([
    [1, 1],
    [1,-1]
    ])

phase = np.array([
    [1,  0],
    [0, 1j]
    ])

t_gate = np.array([
    [1, 0],
    [0, inv_sqrt_2 + inv_sqrt_2 * 1j]
    ])

clifford_generators = [hadamard, phase, t_gate]


