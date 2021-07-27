Fill in this README.md. Example Structure:

## Project Description 
Most quantum applications use qubits to process the information, that means we work on a 2<sup>n</sup>-dimensional Hilbert space since each qubit has 2 accessible states, |0〉 and |1〉. The state of these qubits can be easily modified using gates acting con that Hilbert space. However, we could also use higher energy states, for example we could use qutrits that can be in the states |0〉, |1〉 and |2〉 (or a superposition of those), but now the dimension of the Hilbert space becomes 2<sup>n</sup>3<sup>m</sup> where n is the number of qubits and m is the number of qutrits we have in our system.

In order to manipulate the state of the qutrits we can program directly the microwave pulses that we must apply to the qutrits. When the frequency of the pulse is ressonant with the gap between two energy levels, the population of these states will vary.

The goal of this project is to build a quantum classifier that uses qutrits to distinguish the different classes. The reason for that is because a classifier can be made using a single qubit by checking the fidelity with a set of maximally orthogonal states, if instead we use a qutrit, these states will have a larger orthogonality and therefore we will have less errors.

This classifier uses machine learning techniques and consists on a set of unitary gates parameterized with the rotation angles that must be optimized during the training process via the minimization of a loss function. Each gate will take the previous state and the data of the element we want to classify as inputs and returns a quantum state as the output. Note that the classical data must be re-uploaded in each gate due to the no-cloning theorem of quantum mechanics. The class of the elements is determined when the final's state fidelity with one of the maximally orthogonal states surpasses a certain value.



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

