import itertools
import math
from abc import abstractmethod, ABCMeta
from typing import Union, List, Optional, Dict

import numpy as np
from pyquil import Program, get_qc
from pyquil.api import QuantumComputer
from pyquil.gates import RZ, H, CNOT, MEASURE, RY, CZ

DEFAULT_SHOTS = 10000
DEBUG = False


class ParamCircuitInterface(metaclass=ABCMeta):
    def __init__(self):
        self._circuit: Optional[Program] = None
        self._num_qubits: Optional[int] = None
        self._param_name = list()
        self.num_params = None
        self._result_name = 'ro'

        self._qpu: Optional[QuantumComputer] = None
        self._qpu_name = None
        self._qpu_executable = None

        self._qvm: Optional[QuantumComputer] = None
        self._qvm_executable = None

    @property
    def circuit(self) -> Program:
        if self._circuit is None:
            self._circuit = self._circuit_construction()
        return self._circuit

    @property
    def param_name(self):
        return self._param_name

    def __add__(self, other):
        if not isinstance(other, ParamCircuitInterface):
            raise TypeError
        if self._num_qubits != other._num_qubits:
            raise ValueError
        new_obj = EmptyCircuit()
        new_obj._num_qubits = self._num_qubits
        new_obj._param_name = self._param_name + other._param_name
        new_obj._circuit = self._circuit_construction(add_measure=False) + other._circuit_construction(add_measure=True)
        new_obj._circuit_construction = None
        return new_obj

    @abstractmethod
    def _circuit_construction(self, add_measure=True) -> Program:
        pass

    def set_qpu_backend(self, qc: str):
        p = self.circuit
        self._qpu = get_qc(qc)
        self._qpu_name = qc
        self._qpu_executable = self._qpu.compile(p)

    def run_qpu(self, x: Dict[str, Union[List[float], np.array]],
                qc: Optional[str] = None,
                num_shots: int = DEFAULT_SHOTS):
        self.circuit.wrap_in_numshots_loop(num_shots)
        if self._qpu_name != qc:
            if qc is not None:
                self.set_qpu_backend(qc)
            else:
                print("set qpu backend first.")
                raise RuntimeError
        for p_name in self._param_name:
            for i, v in enumerate(x[p_name]):
                self._qvm_executable.write_memory(region_name=p_name, value=v, offset=i)
        return self._qpu.run(self._qpu_executable).readout_data.get(self._result_name)

    def run_simulation(self, x: Dict[str, Union[List[float], np.array]],
                       num_shots: int = DEFAULT_SHOTS):
        self.circuit.wrap_in_numshots_loop(num_shots)
        assert isinstance(self._num_qubits, int)
        if self._qvm_executable is None:
            self._qvm = get_qc(f"{self._num_qubits}q-qvm")
            self._qvm_executable = self._qvm.compile(self.circuit)
        for p_name in self._param_name:
            for i, v in enumerate(x[p_name]):
                self._qvm_executable.write_memory(region_name=p_name, value=v, offset=i)
        return self._qvm.run(self._qvm_executable).readout_data.get(self._result_name)


class EmptyCircuit(ParamCircuitInterface):
    def _circuit_construction(self, add_measure=True) -> Program:
        raise NotImplementedError


class PauliFeatureMap(ParamCircuitInterface):
    def __init__(self, num_qubits: int, rep: int = 2, param_name="data") -> None:
        super().__init__()
        self._num_qubits = num_qubits
        self._rep = rep
        self._param_name = [param_name]
        self.num_params = num_qubits

    def _circuit_construction(self, add_measure=True) -> Program:
        p = Program()
        param = p.declare(self._param_name[0], "REAL", self.num_params)

        for _ in range(self._rep):
            for i in range(self._num_qubits):
                p.inst(H(i))
                p.inst(RZ(param[i], i))
            for i in range(self._num_qubits - 1):
                p.inst(CNOT(i, i + 1))
                p.inst(RZ((np.pi - param[i]) * (np.pi - param[i + 1]), i + 1))
                p.inst(CNOT(i, i + 1))

        # Measure
        if add_measure:
            ro = p.declare(self._result_name, "BIT", self._num_qubits)
            for i in range(self._num_qubits):
                p.inst(MEASURE(i, ro[i]))
        return p


class VariationalCircuit(ParamCircuitInterface):
    def __init__(self, num_qubits: int, rep: int = 2, param_name="param"):
        super().__init__()
        self._num_qubits = num_qubits
        self._rep = rep
        self._param_name = [param_name]
        self.num_params = rep * (num_qubits - 1) * 4

    def _circuit_construction(self, add_measure=True) -> Program:
        p = Program()
        param = p.declare(self._param_name[0], "REAL", self.num_params)

        param_idx = 0
        for _ in range(self._rep):
            for i in range(self._num_qubits - 1):
                p.inst(RY(param[param_idx], i))
                p.inst(RY(param[param_idx + 1], i + 1))
                p.inst(RZ(param[param_idx + 2], i))
                p.inst(RZ(param[param_idx + 3], i + 1))
                p.inst(CZ(i, i + 1))
                param_idx += 4

        # Measure
        if add_measure:
            ro = p.declare(self._result_name, "BIT", self._num_qubits)
            for i in range(self._num_qubits):
                p.inst(MEASURE(i, ro[i]))
        return p


class AmplitudeEncoding(ParamCircuitInterface):
    def __init__(self, num_amps: int, param_name="beta"):
        super().__init__()
        n = math.log(num_amps, 2)
        assert np.isclose(n, int(n))
        self._num_qubits = int(n)
        self._param_name = [param_name]
        self.num_params = num_amps - 1

    def _circuit_construction(self, add_measure=True) -> Program:
        p = Program()
        betas_flatten = p.declare(self._param_name[0], "REAL", self.num_params)
        n = self._num_qubits
        for s in range(n, 0, -1):
            tot_js = 2 ** (n - s)
            num_combs = math.log(tot_js, 2)
            assert np.isclose(num_combs, int(num_combs)), "Something went wrong"
            num_combs = int(num_combs)
            all_combs = np.array(list(itertools.product([0, 1], repeat=num_combs)))
            for j in range(1, tot_js + 1)[::-1]:
                idx = index_flatten(s, j, n)
                if len(all_combs) == 1:
                    p.inst(RY(betas_flatten[idx], s - 1))
                    # += Program(f"RY({d_betas[s, j]}) {s - 1}")
                else:
                    # pick the relevant combination, e.g. [0,0] or [0, 1] or [1, 0] or [1, 1] for two control qubits
                    comb = all_combs[j - 1]
                    rot_oper_prog_str = f"RY({self._param_name[0]}[{idx}]) "
                    rot_qub_prog_str = f"{s - 1}"
                    flip_prog_strs = []
                    # this loops through the controlled operation, e.g. [0, 1] in the opposite direction
                    for x, cbit in enumerate(comb[::-1]):
                        if cbit == 0:
                            flip_prog_strs += [f"X {s + x}"]
                        else:
                            pass
                        rot_oper_prog_str = "CONTROLLED " + rot_oper_prog_str
                        rot_qub_prog_str = f"{s + x} " + rot_qub_prog_str
                    rot_prog_str = rot_oper_prog_str + rot_qub_prog_str
                    p += Program(flip_prog_strs) + Program(rot_prog_str) + Program(flip_prog_strs[::-1])

        # Measure
        if add_measure:
            ro = p.declare(self._result_name, "BIT", self._num_qubits)
            for i in range(self._num_qubits):
                p.inst(MEASURE(i, ro[i]))
        return p


def flatten_betas(amps, n):
    dct_beta = all_betas(amps)
    flatten_beta = np.zeros(2 ** n - 1)
    for s, j in dct_beta:
        idx = index_flatten(s, j, n)
        flatten_beta[idx] = dct_beta[s, j]
    return flatten_beta


def index_flatten(s, j, n):
    return 2 ** n - 2 ** (n - s + 1) + j - 1


def all_betas(amps):
    """
    Given some real amplitudes, compute the RY angles needed to prepare this state

    :return dict: key: (s, j), value: beta angle
    """
    n = math.log(len(amps), 2)
    assert np.isclose(n, int(n)), f"Specify 2^n amplitudes for some n={n}, amp={amps}"
    n = int(n)
    d_betas = {}
    for s in range(1, n + 1):
        for j in range(1, 2 ** (n - s) + 1):
            # calculate numerator
            numer_sqr = 0.0
            for l in range(2 ** (s - 1)):
                idx_num = (2 * j - 1) * (2 ** (s - 1)) + l
                numer_sqr += np.abs(amps[idx_num]) ** 2
            numerator = np.sqrt(numer_sqr)
            # calculate denominator
            denom_sqr = 0.0
            for ll in range(2 ** s):
                idx_den = (j - 1) * (2 ** s) + ll
                denom_sqr += np.abs(amps[idx_den]) ** 2
            denominator = np.sqrt(denom_sqr)
            # avoid any pathological cases, e.g. if denominator = 0.0
            if np.isclose(numerator, 0.0):
                ratio = 0.0
            else:
                ratio = numerator / denominator
            # ensure argument to arccos lies within domain [-1, 1]
            if ratio > 1.0:
                ratio = 1.0
            elif ratio < -1.0:
                ratio = -1.0
            else:
                pass
            # finally, compute the beta angles
            d_betas[s, j] = -2 * np.arcsin(ratio)
    if DEBUG:
        print(d_betas)
    return d_betas
