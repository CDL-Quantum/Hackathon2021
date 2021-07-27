## Project Description
High-Dimensional Quantum Computing on NISQ devices.

We explore similarities in different quantum hardware and quantum software implementations that leverage multi-level quantum states (qudits).

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

   - IBMQ

   To run jupyter notebooks in the [ibmq](ibmq) folder, activate CDLQ_IBMQ environment and the corresponding jupyter kernel, then install dependencies:
   ```
   conda activate CDLQ_IBMQ
   ipython kernel install --name CDLQ_IBMQ --user
   pip install -r ibmq/requirements.txt
   ```

   - XANADU

   To run jupyter notebooks in the [xanadu](xanadu) folder, activate CDLQ_XANADU environment and the corresponding jupyter kernel, then install dependencies:
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
  - Further walkthrough of what you did
  - Links to any Jupyter notebooks/scripts
  - Business applications
  - Link to Presentation

## References and Further Reading

1. [T.Alexander,N.Kanazawa,D.J.Egger,L.Capelluto,C.J.Wood,A.Javadi-Abhari,D.C.McKay. Qiskit pulse: programming quantum computers through the cloud with pulses](https://iopscience.iop.org/article/10.1088/2058-9565/aba404)
2. [Y.Wang,Z.Hu,B.C.Sanders,S.Kais. Qudits and High-Dimensional Quantum Computing](https://www.frontiersin.org/articles/10.3389/fphy.2020.589504/full)
3. [P.Niemann,R.Wille,R.Drechsler. Equivalence Checking in Multi-level Quantum Systems](http://www.informatik.uni-bremen.de/agra/doc/konf/14_rc_equivalence_checking_multi-level_quantum_systems.pdf)


## Contributors

[Alice Barthe](https://github.com/alice4space), [Henry Makhanov](https://github.com/edenian), [Oleg Fonarev](https://github.com/olegxtend), [Ray Ushnish](https://github.com/ushnishray), [Rodrigo Vargas](https://github.com/RodrigoAVargasHdz)
