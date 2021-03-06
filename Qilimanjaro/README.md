## Project Description 
We have chosen to tackle the *IBM challenge* of the application of qutrits. In our project, we expand on the proposal of a single qubit as a universal classifier by Pérez-Salinas et al. (https://arxiv.org/pdf/1907.02085.pdf) by using a single qutrit instead of a qubit, which should have a higher expressive power because of its higher dimensionality, thus making for a more powerful classifier. The proposed strategy in the paper consists on the *re-uploading of the data points* in order to train our model (check out the aforementioned reference for more details). This is implemented by applying unitary gates to the qutrit, parameterized by the rotation angles, that can be understood as the hidden layers of a neural network. Those rotation angles also include the data that must be re-uploaded in each layer of the classifier. We first tested the classifier by doing some simulations where we trained the model using data generated by us, and we tried implementing it in real quantum hardware. Since the training process is rather time consuming for our current time limit, we could not afford to do the actual training of the physical device. As an attempt to get something closer to the actual experiment, we have generated some predictions with IBM's hardware using the optimal parametrization we have found in our simulations, although these turned out unsuccesful.

## Code files
<ul>
  <li> <code>src/qutrit_classif.ipynb</code> is the hardware implementation of the experiment. </li>
  <li> <code>Qutrit_Classifier_Simulation.ipynb</code> is the simulated qutrit classifier trained with test data. </li>
 </ul>

## Project Details
Most quantum applications use qubits to process the information, that means we work on a 2<sup>n</sup>-dimensional Hilbert space since each qubit has 2 accessible states, |0〉 and |1〉. The state of these qubits can be easily modified using gates acting con that Hilbert space. However, we could also use higher energy states, for example we could use qutrits that can be in the states |0〉, |1〉 and |2〉 (or a superposition of those), but now the dimension of the Hilbert space becomes 2<sup>n</sup>3<sup>m</sup> where n is the number of qubits and m is the number of qutrits we have in our system.

In order to manipulate the state of the qutrits we can program directly the microwave pulses that we must apply to the qutrits. When the frequency of the pulse is ressonant with the gap between two energy levels, the population of these states will vary. This can be done using Qiskit Pulse which lets us program the frequency, amplitude and duration of the pulses we want to apply to our qubits/qutrits.

The goal of this project is to build a quantum classifier that uses qutrits to distinguish the different classes. The reason for that is because a classifier can be made using a single qubit by checking the fidelity with a set of maximally orthogonal states, if instead we use a qutrit, these states will have a larger orthogonality (for the same number of classes > 2) and therefore we will have less errors.

This classifier uses machine learning techniques, it consists on a set of unitary gates parameterized with some coefficients in the rotation angles that must be optimized during the training process via the minimization of a loss function. Each gate will take the previous state and the data of the element we want to classify as inputs and returns a quantum state as the output after weighting these values to get the angle of the unitary rotation. Note that the classical data must be re-uploaded in each gate due to the no-cloning theorem of quantum mechanics that doesn't allow us to copy the data points which are needed in every layer. The class of the elements is determined as the most probable state outcome of the pulse schedule.

Additionally, it is important to mention that it is a good idea to minimize the quantum resources when trying to solve a given problem. In our case, we built a quantum classifier using a single qutrit, and that was possible because of the re-uploading data technique. It would also be possible to build a multi-qutrit classifier with a higher efficiency, but it would be more sophisticated and difficult to implement in larger algorithms.  

The size of the circuit grows linearly with the number of layers, and the number of gates of those layers also grows linearly with the size of the data. The classifier will perform better as we add more layers.


## Gates composition
Applying unitary gates to qutrits is a bit more complex than in qubits, for qubits we have the general U3 matrix given by 

<a href="https://www.codecogs.com/eqnedit.php?latex=U(\theta,&space;\phi,&space;\lambda)=\begin{pmatrix}&space;cos(\theta/2)&space;&&space;-i&space;e^{i&space;\lambda}&space;\sin{(\theta/2)}&space;\\&space;-i&space;e^{i&space;\lambda}&space;\sin{(\theta/2)}&space;&&space;e^{i(\lambda&plus;\phi)}&space;\cos{(\theta/2)}&space;\end{pmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?U(\theta,&space;\phi,&space;\lambda)=\begin{pmatrix}&space;cos(\theta/2)&space;&&space;-i&space;e^{i&space;\lambda}&space;\sin{(\theta/2)}&space;\\&space;-i&space;e^{i&space;\lambda}&space;\sin{(\theta/2)}&space;&&space;e^{i(\lambda&plus;\phi)}&space;\cos{(\theta/2)}&space;\end{pmatrix}" title="U(\theta, \phi, \lambda)=\begin{pmatrix} cos(\theta/2) & -i e^{i \lambda} \sin{(\theta/2)} \\ -i e^{i \lambda} \sin{(\theta/2)} & e^{i(\lambda+\phi)} \cos{(\theta/2)} \end{pmatrix}" /></a>

That can be decomposed as

<a href="https://www.codecogs.com/eqnedit.php?latex=U(\theta,&space;\phi,&space;\lambda)=Z_{\phi-\pi&space;/&space;2}&space;X_{\pi&space;/&space;2}&space;Z_{\pi-\theta}&space;X_{\pi&space;/&space;2}&space;Z_{\lambda-\pi&space;/&space;2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?U(\theta,&space;\phi,&space;\lambda)=Z_{\phi-\pi&space;/&space;2}&space;X_{\pi&space;/&space;2}&space;Z_{\pi-\theta}&space;X_{\pi&space;/&space;2}&space;Z_{\lambda-\pi&space;/&space;2}" title="U(\theta, \phi, \lambda)=Z_{\phi-\pi / 2} X_{\pi / 2} Z_{\pi-\theta} X_{\pi / 2} Z_{\lambda-\pi / 2}" /></a>

We can obtain unitary gates for qutrits by applying 2-dimensional gates to the subspaces {|0〉,|1〉} and {|1〉,|2〉}. By doing so, we can decompose unitary qutrit gates as

<a href="https://www.codecogs.com/eqnedit.php?latex=U=Z_{\varphi_{1}}^{(01)}&space;Z_{\varphi_{2}}^{(12)}&space;Y_{\theta_{1}}^{(12)}&space;Y_{\theta_{2}}^{(01)}&space;Z_{\varphi_{3}}^{(01)}&space;Z_{\varphi_{4}}^{(12)}&space;Y_{\theta_{3}}^{(12)}&space;Z_{\varphi_{5}}^{(01)}&space;Z_{2&space;\varphi_{5}}^{(12)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?U=Z_{\varphi_{1}}^{(01)}&space;Z_{\varphi_{2}}^{(12)}&space;Y_{\theta_{1}}^{(12)}&space;Y_{\theta_{2}}^{(01)}&space;Z_{\varphi_{3}}^{(01)}&space;Z_{\varphi_{4}}^{(12)}&space;Y_{\theta_{3}}^{(12)}&space;Z_{\varphi_{5}}^{(01)}&space;Z_{2&space;\varphi_{5}}^{(12)}" title="U=Z_{\varphi_{1}}^{(01)} Z_{\varphi_{2}}^{(12)} Y_{\theta_{1}}^{(12)} Y_{\theta_{2}}^{(01)} Z_{\varphi_{3}}^{(01)} Z_{\varphi_{4}}^{(12)} Y_{\theta_{3}}^{(12)} Z_{\varphi_{5}}^{(01)} Z_{2 \varphi_{5}}^{(12)}" /></a>

The reason for doing that is because it is not trivial to find the pulses needed for applying a unitary gate to a qutrit, but it is easier to find the pulses corresponding to 2-dimensional X, Y, Z gates. Each subspace has a particular pulse frequency and π-pulse amplitude which need to be determined experimentally. Adressing any of the subspaces is made by setting the correct frequency, and tuning the amplitude and an additional phase allows us to implement a rotation in that subspace.

For our layers we have used only 4 gates:

<a href="https://www.codecogs.com/eqnedit.php?latex=U=&space;Y_{\theta_{1}}^{(12)}&space;X_{\theta_{2}}^{(12)}&space;Y_{\theta_{3}}^{(01)}&space;X_{\theta_{4}}^{(01)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?U=&space;Y_{\theta_{1}}^{(12)}&space;X_{\theta_{2}}^{(12)}&space;Y_{\theta_{3}}^{(01)}&space;X_{\theta_{4}}^{(01)}" title="U= Y_{\theta_{1}}^{(12)} X_{\theta_{2}}^{(12)} Y_{\theta_{3}}^{(01)} X_{\theta_{4}}^{(01)}" /></a>

Where the angles will be determined by the classical data and the weights obtained from the training.

## Results
We started doing some simulations using the qutrit classifier, for that we first generated the training data from the three-class annulus problem. We then used these data points to train our model with 3 layers. 

![image](https://user-images.githubusercontent.com/72504641/127314934-162246ae-9bac-416a-b28c-da3aedca80c0.png)

We wanted to check the accuracy of the model depending on the number of layers, for that we took the percentage of the data that was correctly predicted.

![image](https://user-images.githubusercontent.com/72504641/127315351-b4eb2844-cbbc-4997-85f8-eb877913853b.png)

Finally, as a comparison we plotted the results from a 5 layer model to see the improvement.

![image](https://user-images.githubusercontent.com/72504641/127315529-0476ae20-4564-4f82-929d-9fd344eb11e2.png)






## Setup
1. Make sure to have an IBMid account (which can be created [here](https://www.ibm.com/account/reg/us-en/signup)) that allows you to access the [IBM Quantum Dashboard](https://quantum-computing.ibm.com) in order to find your personal token, which is required to access the IBM Quantum resources used in this project (qpus and simulators).
2. Set up your preferred virtual environment.
3. Run the command `pip install -r requirements.txt` in the `Qilimanjaro` directory to install all the required dependencies.

## How to Use
Run the command `jupyter notebook` in the `Qilimanjaro` directory, inside the `src` folder you will find our two notebooks:
1. `Qutrit_Classifier_Simulation.ipynb` is the simulated qutrit classifier trained with test data.
2. `qutrit_classif.ipynb` is the hardware implementation of the experiment.

## Challenge(s) You Solved

## Project Details: 
  - Further walkthrough of what you did 
  - Links to any Jupyter notebooks/scripts
  - Business applications
  - Link to Presentation

## Contributors 

Qilimanjaro team
