from abc import abstractmethod, ABCMeta
from typing import Union, List, Optional

import numpy as np

from pyquil import Program, get_qc
from pyquil.api import QuantumComputer
from pyquil.gates import RZ, H, CNOT, MEASURE, RY, CZ

"""
from pyquil.parameters import Parameter, quil_sin, quil_cos
from pyquil.quilbase import DefGate
import numpy as np

theta = Parameter('theta')
crx = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, quil_cos(theta / 2), -1j * quil_sin(theta / 2)], [0, 0, -1j * quil_sin(theta / 2), quil_cos(theta / 2)]])

dg = DefGate('CRX', crx, [theta])
CRX = dg.get_constructor()

p = Program()
p.inst(dg)
p.inst(H(0))
p.inst(CRX(np.pi/2)(0, 1))

wavefunction = qvm.wavefunction(p)
print(wavefunction)
"""
DEFAULT_SHOTS = 10000


class ParamCircuitInterface(metaclass=ABCMeta):
    def __init__(self):
        self._circuit: Optional[Program] = None
        self._num_qubits: Optional[int] = None
        self._param_name = 'x'
        self._result_name = 'ro'

        self._qpu: Optional[QuantumComputer] = None
        self._qpu_name = None
        self._qpu_executable = None

        self._qvm: Optional[QuantumComputer] = None
        self._qvm_executable = None

    @property
    def circuit(self) -> Program:
        if self._circuit is not None:
            self._circuit = self._circuit_construction()
        return self._circuit

    @abstractmethod
    def _circuit_construction(self) -> Program:
        pass

    def set_qpu_backend(self, qc: str):
        p = self.circuit
        self._qpu = get_qc(qc)
        self._qpu_name = qc
        self._qpu_executable = self._qpu.compile(p)

    def run_qpu(self, x: Union[List[float], np.array], qc: Optional[str] = None, num_shots: int = DEFAULT_SHOTS):
        self.circuit.wrap_in_numshots_loop(num_shots)
        if self._qpu_name != qc:
            if qc is not None:
                self.set_qpu_backend(qc)
            else:
                print("set qpu backend first.")
                raise RuntimeError
        self._qpu_executable.write_memory(region_name=self._param_name, value=x)
        return self._qpu.run(self._qpu_executable).readout_data.get(self._result_name)

    def run_simulation(self, x: Union[List[float], np.array], num_shots: int = DEFAULT_SHOTS):
        self.circuit.wrap_in_numshots_loop(num_shots)
        assert isinstance(self._num_qubits, int)
        if self._qvm_executable is None:
            self._qvm = get_qc(f"{self._num_qubits}q-qvm")
            self._qvm_executable = self._qvm.compile(self.circuit)
        self._qvm_executable.write_memory(region_name=self._param_name, value=x)
        return self._qvm.run(self._qvm_executable).readout_data.get(self._result_name)


class PauliFeatureMap(ParamCircuitInterface):
    def __init__(self, num_qubits: int, rep: int = 2) -> None:
        super().__init__()
        self._num_qubits = num_qubits
        self._rep = rep

    def _circuit_construction(self) -> Program:
        p = Program()
        ro = p.declare(self._result_name, "BIT", self._num_qubits)
        param = p.declare(self._param_name, "REAL", self._num_qubits)

        for _ in range(self._rep):
            for i in range(self._num_qubits):
                p.inst(H(i))
                p.inst(RZ(param[i], i))
            for i in range(self._num_qubits - 1):
                p.inst(CNOT(i, i + 1))
                p.inst(RZ((np.pi - param[i]) * (np.pi - param[i + 1]), i + 1))
                p.inst(CNOT(i, i + 1))

        # Measure
        for i in range(self._num_qubits):
            p.inst(MEASURE(i, ro[i]))
        return p


class VariationalCircuit(ParamCircuitInterface):
    def __init__(self, num_qubits: int, rep: int = 2):
        super().__init__()
        self._num_qubits = num_qubits
        self._rep = rep

    def _circuit_construction(self) -> Program:
        p = Program()
        ro = p.declare(self._result_name, "BIT", self._num_qubits)
        param = p.declare(self._param_name, "REAL", self._num_qubits)

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
        for i in range(self._num_qubits):
            p.inst(MEASURE(i, ro[i]))
        return p
