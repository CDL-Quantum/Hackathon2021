import qiskit
import numpy as np
from qiskit.algorithms.optimizers import SPSA
from torch.utils.tensorboard import SummaryWriter

class VariationalClassifier:

	def __init__(self, qfm, vc, boolftn, usebias):
		self.qfm = qfm
		self.vc = vc
		self.boolftn = boolftn
		self.usebias = usebias
		if self.usebias:
			self.numparams = len(self.vc.parameters) + 1
		else:
			self.numparams = len(self.vc.parameters)

	def sig(self, x):
		return 1/(1 + np.exp(-1*x))

	def cost(self, TrainData, TrainLabels, numshots, trainparams):

		qasm_backend = qiskit.Aer.get_backend('aer_simulator')
		totcost = 0
		if self.usebias:
			bias = trainparams[-1]
			trainparams = trainparams[:-1]
		else:
			bias = 0

		for datapoint, label in zip(TrainData, TrainLabels):

			# Make the classifier circuit
			totcirc = self.qfm.assign_parameters(datapoint)
			totcirc = totcirc.compose(self.vc.assign_parameters(trainparams))
			totcirc.measure_all()

			# Run the circuit
			totcirc = qiskit.transpile(totcirc, qasm_backend)
			result = qasm_backend.run(totcirc, shots = numshots).result()
			counts = result.get_counts(totcirc)

			# Calculate p_y(x)
			py = 0
			for bitstring in counts:
				if self.boolftn(bitstring) == label:
					py += counts[bitstring]
			py = py / numshots

			# Calculate Error Probability
			ep = self.sig(np.sqrt(numshots) * (0.5 - py + label*bias/2) / np.sqrt(2*(1-py)*py))
			totcost += ep

		return totcost / len(TrainData)

	def train(self, TrainData, TrainLabels, expname):

		# Basic initializations
		trainparams = list(np.ones(self.numparams))
		numshots = 10000

		writer = SummaryWriter('runs/' + expname)
		def callback(nfev, params, fval, stepsize, accept):
			writer.add_scalar('training loss', fval, int(nfev/3))

		def train_cost(trainparams):
			return self.cost(TrainData, TrainLabels, numshots, trainparams)

		# Training Loop
		optimizer = SPSA(maxiter = 250, callback = callback)
		if self.usebias:
			vbds = [(0, 2*np.pi)]*(self.numparams-1) + [(-1, 1)]
		else:
			vbds = [(0, 2*np.pi)]*(self.numparams)
		point, value, nfev = optimizer.optimize(self.numparams, train_cost, variable_bounds = vbds, 
												initial_point = trainparams)
		self.optimparams = point

		return point, value, nfev

	def test(self, TestData, TestLabels):

		# Basic Initializations
		numshots = 10000
		qasm_backend = qiskit.Aer.get_backend('aer_simulator')
		accuracy = 0
		if self.usebias:
			bias = self.optimparams[-1]
			trainparams = self.optimparams[:-1]
		else:
			bias = 0
			trainparams = self.optimparams

		# Calculate for each test datapoint / label
		for datapoint, label in zip(TestData, TestLabels):

			# Make the classifier circuit
			totcirc = self.qfm.assign_parameters(datapoint)
			totcirc = totcirc.compose(self.vc.assign_parameters(trainparams))
			totcirc.measure_all()

			# Run the circuit
			totcirc = qiskit.transpile(totcirc, qasm_backend)
			result = qasm_backend.run(totcirc, shots = numshots).result()
			counts = result.get_counts(totcirc)

			# Calculate p_y(x)
			py = 0
			for bitstring in counts:
				if self.boolftn(bitstring) == label:
					py += counts[bitstring]
			py = py / numshots

			# See if py is large enough to classify correctly
			if py > 1-py - label*bias:
				accuracy += 1
			
		return accuracy / len(TestData)