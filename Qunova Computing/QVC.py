from collections import Counter

import qiskit
import numpy as np
from qcs_api_client.util.errors import QCSHTTPStatusError
from qiskit.algorithms.optimizers import SPSA
from torch.utils.tensorboard import SummaryWriter
import re

DEFAULT_SHOTS = 10000


class VariationalClassifier:

    def __init__(self, qfm, vc, bool_ftn, use_bias):
        self.qfm = qfm
        self.vc = vc
        self.bool_ftn = bool_ftn
        self.use_bias = use_bias
        self.optimal_params = None
        try:
            self.num_params = len(self.vc.parameters)
        except AttributeError:
            self.num_params = self.vc.num_params
        if self.use_bias:
            self.num_params += 1

    @staticmethod
    def sig(x):
        return 1 / (1 + np.exp(-1 * x))

    def cost(self, train_data, train_labels, num_shots=DEFAULT_SHOTS, train_params=None, backend=None, **kwargs):
        tot_cost = 0
        if self.use_bias:
            bias = train_params[-1]
            train_params = train_params[:-1]
        else:
            bias = 0

        for data_point, label in zip(train_data, train_labels):
            py = self._get_py(data_point, label, train_params, backend, num_shots, **kwargs)

            # Calculate Error Probability
            ep = self.sig(np.sqrt(num_shots) * (0.5 - py + label * bias / 2) / np.sqrt(2 * (1 - py) * py))
            tot_cost += ep

        return tot_cost / len(train_data)

    def train(self, train_data, train_labels, exp_name, num_shots=DEFAULT_SHOTS, backend=None, **kwargs):

        # Basic initializations
        train_params = np.ones(self.num_params, dtype=float)

        writer = SummaryWriter('runs/' + exp_name)

        def callback(_nfev, _params, _fval, _step_size, _accept):
            writer.add_scalar('training loss', _fval, int(_nfev / 3))

        def train_cost(_train_params):
            return self.cost(train_data, train_labels, num_shots, _train_params, backend, **kwargs)

        # Training Loop
        optimizer = SPSA(maxiter=250, callback=callback, **kwargs)
        if self.use_bias:
            vbds = [(0, 2 * np.pi)] * (self.num_params - 1) + [(-1, 1)]
        else:
            vbds = [(0, 2 * np.pi)] * self.num_params
        point, value, nfev = optimizer.optimize(self.num_params, train_cost, variable_bounds=vbds,
                                                initial_point=train_params)
        self.optimal_params = point

        return point, value, nfev

    def test(self, test_data, test_label, num_shots=DEFAULT_SHOTS, backend=None, verbose=False, **kwargs):

        # Basic Initializations
        accuracy = 0
        if self.use_bias:
            bias = self.optimal_params[-1]
            train_params = self.optimal_params[:-1]
        else:
            bias = 0
            train_params = self.optimal_params

        # Calculate for each test data_point / label
        py_list = list()
        ans_list = list()
        for data_point, label in zip(test_data, test_label):
            try:
                py = self._get_py(data_point, label, train_params, backend, num_shots, **kwargs)
                # See if py is large enough to classify correctly
                if py > 1 - py - label * bias:
                    accuracy += 1
                    ans_list.append(True)
                else:
                    ans_list.append(False)
                py_list.append(py)
            except QCSHTTPStatusError:
                print("Bad request from QPU. Terminate.")
                if verbose:
                    return accuracy / len(py_list), py_list, ans_list
                else:
                    return accuracy / len(py_list)
        if verbose:
            return accuracy / len(test_data), py_list, ans_list
        else:
            return accuracy / len(test_data)

    def _get_py(self, data_point, label, train_params, backend=None, num_shots=DEFAULT_SHOTS, **kwargs):
        if backend is None:
            backend = qiskit.Aer.get_backend('aer_simulator')

        # Make the classifier circuit
        tot_circ = self.qfm.assign_parameters(data_point)
        tot_circ = tot_circ.compose(self.vc.assign_parameters(train_params))
        tot_circ.measure_all()

        # Run the circuit
        tot_circ = qiskit.transpile(tot_circ, backend)
        result = backend.run(tot_circ, shots=num_shots).result()
        counts = result.get_counts(tot_circ)

        # Calculate p_y(x)
        py = 0
        for bitstring in counts:
            if self.bool_ftn(bitstring) == label:
                py += counts[bitstring]
        py = py / num_shots
        return py


class PyquilVariationalClassifier(VariationalClassifier):
    def _get_py(self, data_point, label, train_params, backend=None, num_shots=DEFAULT_SHOTS, **kwargs):
        qfm_param_name = self.qfm.param_name[0]
        vc_param_name = self.vc.param_name[0]
        input_dict = {qfm_param_name: data_point,
                      vc_param_name: train_params}
        tot_circ = self.qfm + self.vc
        if backend is None or re.match(r"(\d+)q-qvm", backend) is not None:
            # Simulator
            samples = tot_circ.run_simulation(input_dict, num_shots)
        else:
            # QPU
            samples = tot_circ.run_qpu(input_dict, backend, num_shots)
        counts = Counter(["".join(tuple(str(x) for x in y)) for y in samples])

        py = 0
        for bitstring in counts:
            if self.bool_ftn(bitstring) == label:
                py += counts[bitstring]
        py = py / num_shots
        return py
