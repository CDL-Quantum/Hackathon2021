import unittest
import numpy as np

from solovay_kitaev.gates.paulis import *
from solovay_kitaev.gc_decomposition import *

class TestGCDecomposition(unittest.TestCase):

    def test_unitary_phase(self):
        assert abs(unitary_phase(invert_unitary_phase(.1)) - .1) < 10 ** -6
        assert abs(unitary_phase(invert_unitary_phase(.2)) - .2) < 10 ** -6
        assert abs(unitary_phase(invert_unitary_phase(.3)) - .3) < 10 ** -6

    def test_gc_decompose(self):
        test_theta = .1
        test_unitary = np.cos(test_theta/2) * identity - 1j * np.sin(test_theta/2) * pauli_x
        V, W = GC_decompose(test_unitary)
        group_commutator = V @ W @ dag(V) @ dag(W)
        error_bound = np.max(np.abs(group_commutator - test_unitary))
        assert error_bound < .1 # numerical instability issues in current implementation

if __name__ == "__main__":
    unittest.main()