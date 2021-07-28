import numpy as np 
from scipy.optimize import root_scalar
from scipy.linalg import schur
from solovay_kitaev.gates.paulis import *

def dag(matrix : np.ndarray):
    '''
        dag
        Performs a Hermitean conjugate (i.e. conjugate transpose) on the input matrix. Simply returns matrix.conj().T.
        :: matrix : np.ndarray :: Input array; presumed to be a square matrix.
    '''
    return matrix.conj().T


def unitary_phase(phi):
    '''
        unitary_phase
        Returns the solution to Eq. (10) from [DN05] Dawson and Nielsen (2005) -- arXiv:quant-ph/0505030.

        The group commutator produced by solovay_kitaev.gc_decompose can be written as a rotation about some axis by an angle ('theta'). The purpose of this function is to calculate 'theta'. The value of 'theta' depends on the angle ('phi') of rotation about the X and Y axes used as intermediate values for the two unitary operators that, following a basis change, comprise the output of solovay_kitaev.gc_decompose.

        :: phi :: Input angle (or numpy.ndarray of angles) that is assumed to be between 0 and pi/2.
    '''
    # [DN05, Eq. (10)]
    return 2 * np.arcsin(
        2 * (np.sin(phi/2) ** 2) * np.sqrt(
            1 - np.sin(phi/2) ** 4
        )
    )

def invert_unitary_phase(theta):
    '''
        invert_unitary_phase
        Numerically inverts the function solovay_kitaev.unitary_phase. This is needed because we are *given* a unitary phase and we must *calculate* an input that yields that given unitary phase.

        This function is implemented using scipy.root_scalar. The current implementation is quite hacky and so it is NOT VECTORISED.

        :: theta :: Input angle presumed to be the rotation angle for the input unitary of solovay_kitaev.gc_decompose.
    '''
    # Inversion of the theta function
    # warning: this function is NOT VECTORISED
    def fn(phi):
        return unitary_phase(phi) - theta
    solution = root_scalar(fn, bracket=[0, np.pi/2])
    return solution.root


def gc_decompose(unitary, determinant_error=1e-6):
    '''
        gc_decompose
        Implementation of the group commutator decomposition method explained in Section 4.1 of [DN05] Dawson and Nielsen (2005) -- arXiv:quant-ph/0505030. Returns the pair of unitary operators defined in [DN05, Eq. (11)].
        :: unitary           :: Unitary operator to be decomposed. Because of how this unitary operator is processed, the input MUST have determinant 1.
        :: determinant_error :: Error tolerance used when checking that the determinant of the input unitary is 1.
    '''

    #  gc_decompose requires an input with determinant 1.
    assert(np.abs(np.linalg.det(unitary) - 1) < determinant_error)

    eigen_values, _ = np.linalg.eig(unitary)
    coefficient_of_identity = np.real(eigen_values[0])
    output_phase = invert_unitary_phase(2 * np.arccos(coefficient_of_identity))
    
    left_transform = np.cos(output_phase / 2) * identity - 1j * np.sin(output_phase / 2) * pauli_x
    right_transform = np.cos(output_phase / 2) * identity - 1j * np.sin(output_phase / 2) * pauli_y

    group_commutator = left_transform @ right_transform @ dag(left_transform) @ dag(right_transform)

    _, schur_unitary = schur(unitary)
    _, schur_group_commutator = schur(group_commutator)
    similarity_transform = dag(schur_group_commutator) @ schur_unitary

    left_transform = similarity_transform @ left_transform @ dag(similarity_transform)
    right_transform =  similarity_transform @ right_transform @ dag(similarity_transform)
    return left_transform, right_transform
