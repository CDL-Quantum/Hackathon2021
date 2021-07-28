from numpy import array, eye

pauli_x = array([
    [0, 1],
    [1, 0]
    ])

pauli_y = array([
    [0, -1j],
    [1j,  0]
    ])

pauli_z = array([
    [1,  0],
    [0, -1]
    ])  

identity = eye(2)

pauli_generators = [identity, pauli_x, pauli_y, pauli_z]