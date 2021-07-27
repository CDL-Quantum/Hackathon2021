from abc import abstractmethod, ABCMeta, ABC
from typing import Union, List, Optional, Dict

import numpy as np

from pyquil import Program, get_qc
from pyquil.api import QuantumComputer
from pyquil.gates import RZ, H, CNOT, MEASURE, RY, CZ

DEFAULT_SHOTS = 10000


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
            self._qvm_executable.write_memory(region_name=p_name, value=x[p_name])
        return self._qpu.run(self._qpu_executable).readout_data.get(self._result_name)

    def run_simulation(self, x: Dict[str, Union[List[float], np.array]],
                       num_shots: int = DEFAULT_SHOTS):
        self.circuit.wrap_in_numshots_loop(num_shots)
        assert isinstance(self._num_qubits, int)
        if self._qvm_executable is None:
            self._qvm = get_qc(f"{self._num_qubits}q-qvm")
            self._qvm_executable = self._qvm.compile(self.circuit)
        for p_name in self._param_name:
            self._qvm_executable.write_memory(region_name=p_name, value=x[p_name])
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
