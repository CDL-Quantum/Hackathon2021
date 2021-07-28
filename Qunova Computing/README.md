Fill in this README.md. Example Structure:

## Project Description 
(3-4 lines about what it is and how you did it)

## Setup
0. For all file path written in this project, the root directory is `/Qunova Computing/`.

1. Make sure you have [QVM](https://pyquil-docs.rigetti.com/en/v3.0.0/start.html#downloading-the-qvm-and-compiler) installed and configured.

   (Linux) If you counter a trouble that the system can't find `libffi.so.6` when calling `qvm --version` , refer to [here](https://stackoverflow.com/questions/61875869/ubuntu-20-04-upgrade-python-missing-libffi-so-6)
   
2. To use Rigetti QPU, you need to install [QCS-CLI](https://docs.rigetti.com/qcs/guides/using-the-qcs-cli#installation) as well.
3. Set up your preferred virtual environment.

4. `pip install -r requirements.txt`

## How to Use
### 1. Rigetti Challenge
1. Run Jupyter Notebook Server
2. Open two terminals and run `qvm -S` and `quilc -S` for each terminal.
3. **(Data Preprocessing)** Run the [notebook file](./covid19_data/dim_reduc.ipynb) for the preprocessing.
4. **(Training)** Run the [python script file](./training.ipynb) for the training by `python ./traiing_pyquil.py`.

   - You can monitor the training process running `tensorboard --logdir=./runs/zzzpfm_c12v3_zzzpfm_c12v3_pyquil`.
5. **(Testing)** Run the [notebook file](test.ipynb) to test the trained model.
6. **(QPU Testing)** Run the [notebook file](test_qpu.ipynb) to test the trained model on Aspen-9.

## Challenge(s) You Solved
### 1. Rigetti Challenge

The quantum machine learning approach for the hackathon project revolves around two critical papers. 

The first one by V. Havlicek et al. (Supervised learning with quantum enhanced feature spaces, Nature, Vol 567, p 209, 2019) proposes using the quantum state space of a NISQ Computer as a feature space to achieve quantum advantage. We chose to implement the suggested method of a variational quantum classifier.

The basic idea is to map a classical data set with binary labels nonlinearly into a quantum state. Then, we use a variational quantum circuit and perform a binary measurement, allowing the generation of a linear decision function in feature space. The quantum feature map is implemented as a fixed circuit in this approach, while a variational quantum circuit performs the training.

The second paper by S. Lloyd et al. (Quantum embeddings for machine learning, arXiv:2001.03622 (2020)) introduces quantum metric learning as a generalization of the metric learning approach of classical machine learning.  

Here, the basic idea is to train the embedding now to maximize the distance of the data clusters in the Hilbert space of quantum states. The algorithm for the embedding procedure is implemented like the Quantum Approximate Optimization Algorithm (QAOA) of Fahri, Goldstone and Gutman (arXiv:1411.4028).

If the data are clearly separated in Hilbert space, known measurements can be performed to distinguish the different classes. For example, if the data are separated in terms of the trace distance, the Helstrom minimum error measurement can be applied. Similarly, if the distance is measured in terms of the Hilbert-Schmidt norm, the fidelity can be used to measure. This strategy allows for the use of much shorter circuits.


## Project Details: 
### 1. Rigetti Challenge
1. 

  - Further walkthrough of what you did 
  - Links to any Jupyter notebooks/scripts
  - Business applications
  - Link to Presentation


## Contributors 
