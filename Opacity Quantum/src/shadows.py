import numpy as np
import qutip as qt
import scipy as sp

from itertools import product
from functools import reduce

import numpy as np
import qiskit as qk


# ==================================================================
#                  General shadow tomography tools
# ==================================================================

class ShadowTomography:
    """
    A set of tools for performing shadow tomography.

    Parameters
    ----------
    vector: np.ndarray
        Vector representing a quantum state.
    unitaries: list of np.ndarray
        Set of matrices representing unitary transformations.
    basis: list of np.ndarray
        Set of vectors representing measurement results.
    n_shots: int
        Number of measurement shots per element of 'unitaries'.
    """

    def __init__(self, vector: np.ndarray, unitaries: list, basis: list, n_shots: int, measurements=None, shadows = None, estimators = None):
        self.vector = vector
        self.unitaries = unitaries
        self.basis = basis
        self.n_shots = n_shots

        # These variables will be calculated when their respective functions are used if unspecified
        self.measurements = measurements
        self.shadows = shadows
        self.estimators = estimators

        # Pre-calculate the quantum channel for the method.
        self.channel = self.calculate_channel()

    def calculate_channel(self):
        """
        Calculates the quantum channel that describes the experimental method.
        """

        # Calculate the channel that describes measurement in the computational basis.
        M_Z = sum([sp.sparse.kron(b, b.conj().T) for b in self.basis])

        # Calculate the twirl of the measurement channel for the specified set of unitaries.
        M = sum([U.conj().T @ M_Z @ U for U in self.unitaries]) / len(self.unitaries)

        return M

    def simulate_measurements(self):
        """
        Simulates measurement results for the experiment.
        """

        # Measure the state after applying each unitary transformation.
        b = []
        for U in self.unitaries:
            b.append(
                [measure(U @ self.vector, self.basis) for _ in range(self.n_shots)]
            )

        # Store the measurements.
        self.measurements = b

        return b

    def calculate_shadows(self):
        """
        Calculates classical shadows from the stored measurements.
        """

        # If there are no stored measurements, simulate them.
        if isinstance(self.measurements, type(None)):
            self.simulate_measurements()

        # Calculate the inverse of the channel for the experiment.
        M_inv = pinv_d(self.channel)

        # Calculate the classical shadow corresponding to each measurement.
        S = []
        for j, U in enumerate(self.unitaries):
            for k in range(self.n_shots):
                S.append(
                    M_inv @ U.conj().T @ self.measurements[j][k]
                )

        # Store the shadows.
        self.shadows = S

        return S

    def calculate_estimators(self, n_estimators: int):
        """
        Calculates a set of estimators from a set of shadows.

        Parameters
        ----------
        n_estimators: int
            Number of estimators.
        """

        # If no shadows are stored, calculate them.
        if isinstance(self.shadows, type(None)):
            self.calculate_shadows()

        # Shuffle the order of the shadows.
        np.random.shuffle(self.shadows)

        # Number of shadows to average for each estimator.
        r = len(self.shadows) // n_estimators

        # Average the shadows into a set of estimators.
        E = []
        for j in range(n_estimators):
            E.append(
                sum(self.shadows[j * r:(j + 1) * r]) / float(r)
            )

        # Store the estimators
        self.estimators = E

        return E


# ==================================================================
#                          Useful functions
# ==================================================================


def measure(state, basis):
    """
    Simulates the projective measurement of a quantum state.

    Parameters
    ----------
    state: np.ndarray
        Vectorised density matrix of a quantum state.
    basis: list of np.ndarray
        List of (vectorised) projectors onto basis states.
    """

    # Calculate the probabilities for measuring the state in each basis state.
    probs = np.array([])
    for b in basis:
        probs = np.append(
            probs,
            abs(sum((b.conj().T @ state).diagonal()))
        )

    # Normalise the probabilities.
    probs = probs / sum(probs)

    # Choose the index of the state to project onto, weighted by the probabilities.
    j = np.random.multinomial(1, probs).argmax()

    return basis[j]


def expectation_value(state, operator):
    """
    Calculates the expectation value of a superoperator for a quantum state.

    Parameters
    ----------
    state: np.ndarray
        Vectorised density matrix of a quantum state.
    operator: list of np.array
        Quantum superoperator.
    """

    return sum((state.conj().T @ operator @ state).diagonal())


def fidelity(x, y):
    """
    Calculates the fidelity of two vectors.

    Parameters
    ----------
    x: np.array
        Vector.
    y: np.array
        Vector.
    """

    return abs(sum((x.conj().T @ y).diagonal()))


def average_distance(x, y):
    """
    Calculates the average distance between two vectors.

    Parameters
    ----------
    x: np.array
        Vector.
    y: np.array
        Vector.
    """

    return np.linalg.norm(x - y) / len(x)


def str_to_index(s):
    """
    Converts an n-qutrit result string into its index in the n-qutrit computational basis.

    Parameters
    ----------
    s: str
        Measurement result of a quantum circuit.
    """

    return int("".join(i for i in s), 2)


# ==================================================================
#                           Reshaping tools
# ==================================================================


def vec(tensor):
    """
    Vectorises a tensor.

    Parameters
    ----------
    tensor: np.array
        Tensor with arbitrary dimensions.
    """
    return tensor.reshape(-1, 1)


# ==================================================================
#                         Superoperator tools
# ==================================================================


def to_super(operator):
    """
    Promotes an operator to a superoperator.

    Parameters
    ----------
    operator: np.array
        Quantum operator.
    """

    return sp.sparse.kron(operator, operator.conj())


# ==================================================================
#                           Qutrit operators
# ==================================================================

def rx_level_i(theta, level_i, n_levels=3, qutip=False):
    """
    Returns the single qubit x-rotation in the 2-level
    subsystem between |level_i> and |level_i+1> defined on a
    qudit of size n_levels
    """

    R = np.array([[np.cos(theta / 2), -1j * np.sin(theta / 2)],
                  [-1j * np.sin(theta / 2), np.cos(theta / 2)]])
    G = np.eye(n_levels) + 0j * np.eye(n_levels)
    G[level_i:level_i + 2, level_i:level_i + 2] = R
    if qutip:
        return qt.Qobj(G, dims=[[n_levels]] * 2)
    else:
        return sp.sparse.csc_matrix(G)


def ry_level_i(theta, level_i, n_levels=3, qutip=False):
    """
    Returns the single qubit y-rotation in the 2-level
    subsystem between |level_i> and |level_i+1> defined on a
    qudit of size n_levels
    """

    R = np.array([[np.cos(theta / 2), -np.sin(theta / 2)],
                  [np.sin(theta / 2), np.cos(theta / 2)]])
    G = np.eye(n_levels) + 0j * np.eye(n_levels)
    G[level_i:level_i + 2, level_i:level_i + 2] = R
    if qutip:
        return qt.Qobj(G, dims=[[n_levels]] * 2)
    else:
        return sp.sparse.csc_matrix(G)


# ==================================================================
#                           Operator bases
# ==================================================================

def _equivalent_operator(O1, O2):
    return np.isclose((vec(O1).T.conj() @ vec(O2))[0, 0], 3)


def paulis(minimal=False):
    """
    Returns a list of the single-qutrit Pauli operators
    """
    # way too big but MVP
    X01 = rx_level_i(np.pi, 0)
    X12 = rx_level_i(np.pi, 1)
    Y01 = ry_level_i(np.pi, 0)
    Y12 = ry_level_i(np.pi, 1)
    ps = []
    for (i, j, k, l) in product(range(4), repeat=4):
        # generate an element
        P = (X01 ** i) * (X12 ** j) * (Y01 ** k) * (Y12 ** l)
        # don't add equivalent operators in and skip identity - This will slow things down but speed us up if we are
        # going to multiple sites
        if minimal:
            if not any([_equivalent_operator(P, p) for p in ps]) and not _equivalent_operator(P, np.eye(3)):
                ps.append(P)
        else:
            ps.append(P)
    return ps


def cliffords(minimal=False):
    """
    Returns a list of the single-qutrit Clifford operators
    """
    # way too big but MVP
    cs = []
    X01 = rx_level_i(np.pi / 2, 0)
    X12 = rx_level_i(np.pi / 2, 1)
    Y01 = ry_level_i(np.pi / 2, 0)
    Y12 = ry_level_i(np.pi / 2, 1)
    for (i, j, k, l) in product(range(4), repeat=4):
        # generate an element
        P = (X01 ** i) * (X12 ** j) * (Y01 ** k) * (Y12 ** l)
        # don't add equivalent operators in and skip identity - This will slow things down but speed us up if we are
        # going to multiple sites
        if minimal:
            if not any([_equivalent_operator(P, p) for p in cs]) and not _equivalent_operator(P, np.eye(3)):
                cs.append(P)
        else:
            cs.append(P)
    return cs


# ==================================================================
#                      N-qutrit states/operators
# ==================================================================


def computational_basis(n_qutrits=1):
    """
    List of the n-qutrit computational basis states.

    Parameters
    ----------
    n_qutrits: int
        Number of qutrits.
    """

    # Single-qutrit logical basis states.
    logicals = [sp.sparse.csc_matrix(qt.basis(3, i).full()) for i in range(3)]

    return [reduce(sp.sparse.kron, j) for j in product(logicals, repeat=n_qutrits)]


def nqutrit_operators(n_qutrits, operators):
    """
    List of n-qutrit tensor products of the single-qutrit operators.

    Parameters
    ----------
    n_qutrits: int
        Number of qutrits.
    operators: list of np.array
        Set of single-qutrit operators.
    """

    return [reduce(sp.sparse.kron, j) for j in product(operators, repeat=n_qutrits)]


def delta_eye(X, delta):
    # add a small delta * Id offset for inverse
    return X + delta * np.eye(X.shape[0])


def pinv_d(X, delta=1e-13, rcond=1e-20, hermitian=True):
    # robust pinv for ill-conditioned matrices
    return np.linalg.pinv(delta_eye(X, delta), rcond=rcond, hermitian=hermitian)

