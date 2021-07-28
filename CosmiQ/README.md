## Project Description
High-Dimensional Quantum Computing on NISQ devices.

We explore similarities between different quantum hardware and quantum software implementations and leverage multi-level quantum states (qudits) for solving a financial portfolio optimization problem.

## Setup
In order to facilitate online collaboration, the CosmiQ team used [mybinder.org](https://mybinder.readthedocs.io/en/latest/introduction.html) free online service. See [binder/README](binder/README.md) file for more details.

For local installations, please follow the instructions below.

1. Make sure you have python 3.8+, pip and JupyterLab installed and configured.
2. Set up your preferred virtual environment, e.g.:
```
python3 -m venv cdl
source cdl/bin/activate
```
3. Configure two conda environments to install vendor specific dependencies, e.g.:
```
conda create -n CDLQ_IBMQ python=3
conda create -n CDLQ_XANADU python=3
```
4. Activate corresponding environment and load vendor specific dependencies before starting `jupyter notebook` in each of the subfolders:

   - *__IBMQ__*

   To run the Jupyter notebooks in the [ibmq](ibmq) folder, activate CDLQ_IBMQ environment and the corresponding jupyter kernel, then install dependencies:
   ```
   conda activate CDLQ_IBMQ
   ipython kernel install --name CDLQ_IBMQ --user
   pip install -r ibmq/requirements.txt
   ```

   - *__XANADU__*

   To run the Jupyter notebooks in the [xanadu](xanadu) folder, activate CDLQ_XANADU environment and the corresponding jupyter kernel, then install dependencies:
   ```
   conda activate CDLQ_XANADU
   ipython kernel install --name CDLQ_XANADU --user
   pip install -r xanadu/requirements.txt
   ```

## Challenges We Solved

We addressed two challenges in this project:

1. IBM Q’s Challenge
2. Xanadu’s Challenge

Please refer to the [CDL Quantum Hackathon 2021 README file](../README.md) for more details.

## Project Details:

  - To address **IBM Q's Challenge**, we used Qiskit Pulse to calibrate a three-level quantum device on ibmq_armonk and to construct a full set of single-qutrits logical gates.

  The IBM Q's Challenge solution overview including references to related Python code and Jupyter notebooks can be found in the [IBMQ Challenge Solution Overview](IBMQ_challenge_solution.md) file.

  - To **address Xanadu's Challenge**, we .....

  The Xanadu's Challenge solution overview including references to related Python code and Jupyter notebooks can be found in the [Xanadu Challenge Solution Overview](Xanadu_challenge_solution.md) file.

  - Business applications - **TODO**
  - Link to Presentation - [CosmiQ Presentation](https://docs.google.com/presentation/d/11hNlrG5h4nE9QYco3dloQPALMRBJFJ-N-VslGnBzO68/edit?usp=sharing)


## Contributors

[Alice Barthe](https://github.com/alice4space), [Henry Makhanov](https://github.com/edenian), [Oleg Fonarev](https://github.com/olegxtend), [Ray Ushnish](https://github.com/ushnishray), [Rodrigo Vargas](https://github.com/RodrigoAVargasHdz)
