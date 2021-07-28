Fill in this README.md. Example Structure:

## Project Description 
Most quantum applications use qubits to process the information, that means we work on a 2<sup>n</sup>-dimensional Hilbert space since each qubit has 2 accessible states, |0〉 and |1〉. The state of these qubits can be easily modified using gates acting con that Hilbert space. However, we could also use higher energy states, for example we could use qutrits that can be in the states |0〉, |1〉 and |2〉 (or a superposition of those), but now the dimension of the Hilbert space becomes 2<sup>n</sup>3<sup>m</sup> where n is the number of qubits and m is the number of qutrits we have in our system.

In order to manipulate the state of the qutrits we can program directly the microwave pulses that we must apply to the qutrits. When the frequency of the pulse is ressonant with the gap between two energy levels, the population of these states will vary. This can be done using Qiskit Pulse which lets us program the frequency, amplitude and duration of the pulses we want to apply to our qubits/qutrits.

The goal of this project is to build a quantum classifier that uses qutrits to distinguish the different classes. The reason for that is because a classifier can be made using a single qubit by checking the fidelity with a set of maximally orthogonal states, if instead we use a qutrit, these states will have a larger orthogonality and therefore we will have less errors.

This classifier uses machine learning techniques, it consists on a set of unitary gates parameterized with some coefficients in the rotation angles that must be optimized during the training process via the minimization of a loss function. Each gate will take the previous state and the data of the element we want to classify as inputs and returns a quantum state as the output after weighting these values to get the angle of the unitary rotation. Note that the classical data must be re-uploaded in each gate due to the no-cloning theorem of quantum mechanics that doesn't allow us to copy the data points which are needed in every layer. The class of the elements is determined when the final's state fidelity with one of the maximally orthogonal states surpasses a certain value.

Additionally, it is important to mention that it is a good idea to minimize the quantum resources when trying to solve a given problem. In our case, we built a quantum classifier using a single qutrit, and that was possible because of the re-uploading data technique. 

The size of the circuit grows linearly with the number of layers, and the number of gates of those layers also grows linearly with the size of the data. The classifier will perform better as we add more layers.


Applying unitary gates to qutrits is a bit more complex than in qubits, for qubits we have the U3 matrix given by 
<a href="https://www.codecogs.com/eqnedit.php?latex=U(\theta,&space;\phi,&space;\lambda)=\begin{pmatrix}&space;cos(\theta/2)&space;&&space;-i&space;e^{i&space;\lambda}&space;\sin{(\theta/2)}&space;\\&space;-i&space;e^{i&space;\lambda}&space;\sin{(\theta/2)}&space;&&space;e^{i(\lambda&plus;\phi)}&space;\cos{(\theta/2)}&space;\end{pmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?U(\theta,&space;\phi,&space;\lambda)=\begin{pmatrix}&space;cos(\theta/2)&space;&&space;-i&space;e^{i&space;\lambda}&space;\sin{(\theta/2)}&space;\\&space;-i&space;e^{i&space;\lambda}&space;\sin{(\theta/2)}&space;&&space;e^{i(\lambda&plus;\phi)}&space;\cos{(\theta/2)}&space;\end{pmatrix}" title="U(\theta, \phi, \lambda)=\begin{pmatrix} cos(\theta/2) & -i e^{i \lambda} \sin{(\theta/2)} \\ -i e^{i \lambda} \sin{(\theta/2)} & e^{i(\lambda+\phi)} \cos{(\theta/2)} \end{pmatrix}" /></a>

## Setup
Example:
1. Make sure you have X installed and configured.

2. Set up your preferred virtual environment.

3. pip install -r requirements.txt

## How to Use
Example:
From command line: Use python solvers/script.py -h

## Challenge(s) You Solved

## Project Details: 
  - Further walkthrough of what you did 
  - Links to any Jupyter notebooks/scripts
  - Business applications
  - Link to Presentation

## Contributors 

