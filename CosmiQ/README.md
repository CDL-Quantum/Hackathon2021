## Project Description

Higher Dimensional Quantum Computing on NISQ devices, use case : Qutrit for Finance

We implement a library to manipulate Qutrit at pulse level on IBM Q pulse. We also explore similarities between different quantum hardware and quantum software implementations and leverage multi-level quantum states (qudits) for solving a financial portfolio optimization problem.

## Challenges

We addressed three challenges in this project:

1. IBM Q’s Challenge
2. Xanadu’s Challenge
3. D-Wave's Challenge

Please refer to the [CDL Quantum Hackathon 2021 README file](../README.md) for more details.

## Project Details:

  - To address **IBM Q's Challenge**, we used Qiskit Pulse to calibrate a three-level quantum device on ibmq_armonk and to construct a full set of single-qutrits logical gates. The IBM Q's Challenge solution overview including references to related Python code and Jupyter notebooks can be found in the [IBMQ Challenge Solution Overview](IBMQ_challenge_solution.md) file.

  - To address **Xanadu's Challenge**, we used Pennylane to solve a portfolio trajectory optimization. The Xanadu's Challenge solution overview including references to related Python code and Jupyter notebooks can be found in the [Xanadu Challenge Solution Overview](Xanadu_challenge_solution.md) file.

  - To address **D-Wave's Challenge**, we reformulated a famous partitioning QUBO into a QUTO (quadratic unconstrained binary/ternary optimisation) and showed the complexity reduction associated. It was solved using the D-Wave libraries. The D-Wave's Challenge solution overview including references to related Python code and Jupyter notebooks can be found in the [D-Wave Challenge Solution Overview](DWave_challenge_solution.md) file.

  - Business applications - please refer to the Business Section in the [Xanadu Challenge Solution Overview](Xanadu_challenge_solution.md) file.

  - Link to Presentation - [CosmiQ Presentation](https://docs.google.com/presentation/d/11hNlrG5h4nE9QYco3dloQPALMRBJFJ-N-VslGnBzO68/edit?usp=sharing)
  - To install the directory please refer to the [installation guide](installation_guide.md).


## Contributors

[Alice Barthe](https://github.com/alice4space), [Henry Makhanov](https://github.com/edenian), [Oleg Fonarev](https://github.com/olegxtend), [Ray Ushnish](https://github.com/ushnishray), [Rodrigo Vargas](https://github.com/RodrigoAVargasHdz)
