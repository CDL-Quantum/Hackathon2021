README.md - RNA Diagnosis for Virus Infection

## Project Description 

Infected by a virus, a biosystem manifest RNA test signals differently from that 
of healthy one. However, not all RNA responses to virus infection. During the 
COVID-19 Pandemic period, the test kit had to be developed rapidly to identify 
patients with COVID-19 infection. An RNA test is provided by the PCR method, which
amplifies the chemical signal of existence of a certain RNA. The test kit measures 
the concentration of 100s of different RNAs to identify infected cases. 

Here comes the question - What RNAs to look into ?

Finding the answer to this question requires a comprehensive analysis of the RNA 
property of millions of candidate RNAs. It may take years if we don't know much 
about the new viruses.

In this hackathon project, we have applied variational perceptron circuit learning
with feature space data embedding. More detailed description can be found the 
tha main body of this report. 

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
### 1. Rigetti Challenge for Identifying RNAs for COVID19 PCR Test

#### Problem Description

A quantum machine learning can quickly classify which RNAs to look at from the 
RNA PCR data with and without COVID19 infections. In the beginning of the COVID19 
Pandemic, researchers have rapidly built up the metadata of COVID19 RNA test. One 
good data repository can be found at https://www.genome.jp/kegg/pathway.html.

We chose 102 RNAs which may not or may be reactive to COVID19 on KEGG pathway 
hsa05171 and 6 different transcriptomes from cells with and without 
COVID19 infection. The training sample structure is shown below:

![Figure](./figures/RNAtranscriptome.png)

Here we utilize the quantum machine learning to classify the RNAs that are sensitive 
to COVID19 for the test kit development. 

The quantum machine consists of two major sub-circuits: Data embedding circuit
and variational perceptron circuit. Due to the nature of variational circuit with 
learning variable parameter theta, the circuit is repeatedly executed to find 
the parameter with SPSA optimizer. Here we set the loss function by Hilbert-Schmidt 
distance.

#### Data Embedding 

The embedding of the data can be efficiently achieved when we map the classical data
onto a feature map space. The basic idea is taken from the paper
by V. Havlicek et al. (Supervised learning with quantum enhanced 
feature spaces, Nature, Vol 567, p 209, 2019) proposes using the quantum state 
space of a NISQ Computer as a feature space to achieve quantum advantage. This 
idea can embed the data into a feature space with relatively short circuit length. 

The basic idea is to map a classical data set with binary labels non-linearly into 
a quantum state. Then, we use a variational quantum circuit and perform a binary 
measurement, allowing the generation of a linear decision function in feature space. The quantum feature map is 
implemented as a fixed circuit in this approach, while a variational 
quantum circuit performs the training.

For the detail implementation, you can refer to the following the [python file](https://github.com/QuNovaComputing/Hackathon2021/blob/qunovacomputing/Qunova%20Computing/pyquil_circuits.py#L96).

#### Classification by Variation Quantum Perceptron Circuit 

The machine learning part is achieved by the variational perceptron quantum 
classifier idea is taken from the paper by S. Lloyd et al. (Quantum embeddings 
for machine learning, [arXiv:2001.03622](https://arxiv.org/abs/2001.03622) (2020)) introduces quantum metric learning as a generalization 
of the metric learning approach of classical machine learning.  

Here, the basic idea is to train the embedding now to maximize the distance of 
the data clusters in the Hilbert space of quantum states. The algorithm for the 
embedding procedure is implemented like the Quantum Approximate Optimization 
Algorithm (QAOA) of Fahri, Goldstone and Gutman ([arXiv:1411.4028](https://arxiv.org/abs/1411.4028)).

If the data are clearly separated in Hilbert space, known measurements can be 
performed to distinguish the different classes. For example, if the data are 
separated in terms of the trace distance, the Helstrom minimum error measurement 
can be applied. Similarly, if the distance is measured in terms of the 
Hilbert-Schmidt norm, the fidelity can be used to measure. This strategy 
allows for the use of much shorter circuits.

For the detail implementation, you can refer to the follwing following the [python file](https://github.com/QuNovaComputing/Hackathon2021/blob/qunovacomputing/Qunova%20Computing/pyquil_circuits.py#L125).


#### Preprocessing of the data

Before the embedding the data, we used classical PCA(principal component analysis) to reduce the data dimension, which 
is demonstrated in this [notebook file](./covid19_data/dim_reduc.ipynb).

#### Quantum Amplitude Encoding

We also adapted the amplitude encoding scheme introduced in the [skeleton code](./rigetti_resources/Amplitude%20Encoding.ipynb),
But running out of the time, we couldn't train the variational circuit with this encoding scheme.
This [notebook file](./amp_encoding_training.ipynb) demonstrates the training with amplitude encoding.

## Contributors 

Qunova Computing Team
- [Kevin June-Koo Rhee](https://github.com/rheejk84)
- [Gwonhak Lee](https://github.com/snow0369)
- [Minjin Choi](https://github.com/QunovaCMJ)
- [Francesco Petruccione](https://github.com/petruccione)
- Whie Willy Chang