import unittest
from numpy import array, eye 

from solovay_kitaev.basic_approximation import basic_approximation_generator, BaseCaseQuery
from solovay_kitaev.gates import cliffords

class TestBasicApproximation(unittest.TestCase):

    def test_empty(self):
        try:
            for i in basic_approximation_generator():
                print(i)
        except IndexError:
            pass
        return

    def test_simple(self):
        gates = cliffords.clifford_generators
        gates.append(eye(2)) # Add the identity
        base_cases = list(basic_approximation_generator(*gates, depth=1))

        for case in base_cases:
            gate_found = False
            for gate in gates:
                if (gate == case[0]).all():
                    gate_found = True
                    break
            assert(gate_found)

        return

    def test_construct_query_structure(self):
        gates = cliffords.clifford_generators
        gates.append(eye(2)) # Add the identity

        BaseCaseQuery(*gates)

        return

    def test_query(self):
        gates = cliffords.clifford_generators
        gates.append(eye(2)) # Add the identity

        base_case = BaseCaseQuery(*gates)

        assert(len(base_case(eye(2))) == 2)

        for gate in gates:
            assert((base_case(gate)[0] == gate).all())

        return

            

if __name__ == "__main__":
    unittest.main()
