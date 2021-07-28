import numpy as np
from solovay_kitaev.gc_decomposition import gc_decompose, dag
from solovay_kitaev.basic_approximation import BaseCaseQuery

def solovay_kitaev(
        unitary: np.ndarray,
        depth: int,
        gates = None : list # TODO import gates and include appropriate defaults, expand to *args
        ) -> np.ndarray, list:
    '''
        solovay_kitaev
        Function to implement the Solovay Kitaev algorithm
        Takes in a unitary to approximate along with a maximal depth
        :: unitary : array :: The unitary to approximate
        :: depth   : int   :: The maximum depth of the approximation
        :: gates   : array :: The set of basis gates
        Returns the approximation of the unitary along with a 
        list of the gates that provide the approxmiation
    '''

    if gates is None:
        raise(NotImplementedError)

    basic_approximation = BaseCaseQuery(*gates, depth=depth)

    if depth == 0:
        return basic_approximation(unitary)
    else:
        previous_unitary = solovay_kitaev(unitary, depth-1, gates=gates)
        V, W = gc_decompose(unitary @ dag(previous_unitary))
        prev_V = solovay_kitaev(V, *gates, depth - 1, gates=gates)
        prev_W = solovay_kitaev(W, *gates, depth - 1, gates=gates)
        group_commutator = V @ W @ dag(V) @ dag(W)
        return group_commutator @ previous_unitary
