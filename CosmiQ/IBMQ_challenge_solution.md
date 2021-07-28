# IBM Q's Challenge Solution Overview

## Qutrits

The majority of existing quantum algorithms are based on qubits, 2-level systems with the ![0_state](https://latex.codecogs.com/gif.latex?%7C%200%20%5Crangle%20%3D%20%5B0%2C1%5D) and ![1_state](https://latex.codecogs.com/gif.latex?%7C%201%20%5Crangle%20%3D%20%5B1%2C0%5D).
Corresponding gate operations can be composed from single-qubit gates, and two-qubits gates; for example, the *Pauli-X* rotates the state ![1_state](https://latex.codecogs.com/gif.latex?%7C%201%20%5Crangle) to ![0_state](https://latex.codecogs.com/gif.latex?%7C%200%20%5Crangle); ![Pauli_eq](https://latex.codecogs.com/gif.latex?X%20%7C%201%20%5Crangle%20%3D%20%7C%200%20%5Crangle).

As it was pointed out in Ref. [1], quantum computing could also be done using multi-level quantum systems (**qudits**) as the building block in quantum information.
Why bother using qudits? It has been theoretically illustrated (Ref. [2]) that qudits-based quantum systems can store and processes information more efficiently than those using only qubits.
A natural question arises, how to engineer qudits?. For example, cold molecules in ultra cold temperatures have non-degenerate states  under the presence of an external electric field (Stark shift), Ref. [3].
Nonetheless, it would be ideal to design qudits taking advantage of the current architectures, for example, superconducting quantum processors.

Qutrits are qudits that are constructed from quantum states like spin-1 systems, where the basis is ![](https://latex.codecogs.com/gif.latex?%7C0%5Crangle%2C%7C1%5Crangle) and ![](https://latex.codecogs.com/gif.latex?%7C2%5Crangle).
In order to have a universal quantum computer based on qutris, we need to have a well defined set of gates.
For example, the ***X*** gates are,

>
>![X qtrits gates](https://latex.codecogs.com/gif.latex?X%5E%7B%2801%29%7D%20%3D%20%5Cbegin%7Bpmatrix%7D%200%20%26%201%20%26%200%20%5C%5C%201%20%26%200%20%26%200%5C%5C%200%20%26%200%20%26%201%20%5Cend%7Bpmatrix%7D%20%5C%3B%5C%3B%5C%3B%20X%5E%7B%2802%29%7D%20%3D%20%5Cbegin%7Bpmatrix%7D%200%20%26%200%20%26%201%20%5C%5C%200%20%26%201%20%26%200%5C%5C%201%20%26%200%20%26%200%20%5Cend%7Bpmatrix%7D%5C%3B%5C%3B%5C%3B%20X%5E%7B%2812%29%7D%20%3D%20%5Cbegin%7Bpmatrix%7D%201%20%26%200%20%26%200%20%5C%5C%200%20%26%200%20%26%201%20%5C%5C%200%20%26%201%20%26%200%20%5Cend%7Bpmatrix%7D)
>

and the Hadamard gates are given by,

>
>![](https://latex.codecogs.com/gif.latex?%5Csmall%20H%5E%7B%2801%29%7D%20%3D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%7D%7D%5Cbegin%7Bpmatrix%7D%201%20%26%201%20%26%200%20%5C%5C%20-1%20%26%201%20%26%200%5C%5C%200%20%26%200%20%26%20%5Csqrt%7B2%7D%20%5Cend%7Bpmatrix%7D%20%5C%3B%5C%3B%5C%3BH%5E%7B%2802%29%7D%20%3D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%7D%7D%5Cbegin%7Bpmatrix%7D%201%20%26%200%20%26%201%20%5C%5C%201%20%26%20%5Csqrt%7B2%7D%20%26%200%5C%5C%20a%20%26%200%20%26%20-1%20%5Cend%7Bpmatrix%7D%20%5C%3B%5C%3B%5C%3B%20X%5E%7B%2812%29%7D%20%3D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%7D%7D%5Cbegin%7Bpmatrix%7D%20%5Csqrt%7B2%7D%20%26%200%20%26%200%20%5C%5C%200%20%26%201%20%26%201%20%5C%5C%200%20%26%20-1%20%26%201%20%5Cend%7Bpmatrix%7D)   
>

## Calibrating qubits and qutrits and creating single-qutrit gates using Qiskit Pulse

In this project, we make use of Qiskit Pulse to calibrate individual IBM Q's transmon qubits for the first and the second excited states.

The approach is based on a few observations.

1. A transmon qubit can be modelled using a Hamiltonian that describes the Duffing oscillator,

>
>![Duffing Oscillator Hamiltonian](https://latex.codecogs.com/gif.latex?H%20%3D%20%5Comega%20a%5E%5Cdagger%20a%20&plus;%20%5Cfrac%7B%5Calpha%7D%7B2%7D%20a%5E%5Cdagger%20a%5E%5Cdagger%20a%20a)
>

  where ![omega](https://latex.codecogs.com/gif.latex?%5Comega) gives the ![zero-to-one](https://latex.codecogs.com/gif.latex?0%5Crightarrow1) excitation frequency (![](https://latex.codecogs.com/gif.latex?%5Comega%20%5Cequiv%20%5Comega%5E%7B0%5Crightarrow1%7D)) and ![alpha](https://latex.codecogs.com/gif.latex?%5Calpha) is the anharmonicity between the ![zero-to-one](https://latex.codecogs.com/gif.latex?0%5Crightarrow1) and ![one-to-two](https://latex.codecogs.com/gif.latex?1%5Crightarrow2) frequencies (![alpha_is_delta_omega](https://latex.codecogs.com/gif.latex?%5Calpha%20%5Cequiv%20%5Comega%5E%7B1%5Crightarrow2%7D%20-%20%5Comega%5E%7B0%5Crightarrow1%7D)).

![Duffing oscillator](ibmq/images/Anharmonic_oscillator.gif)

Figure used with permission from Wikipedia

Typical single-qubit calibration and classification experiments are used to extract information about the quantum device, such as oscillator frequencies and amplitudes. This information can be used to construct high-fidelity logical gates, perform error corrections, etc.

2. In the calibration experiment, a series of microwave pulses (frequency sweep) is applied to a qubit in order to determine the qubit frequency, i.e. the difference between the first excited state and the ground state.

The calibration experiment can be carried out by creating a Gaussian pulse schedule with fixed duration, sigma and amplitude, and then applying it to a given qubit by varying the frequency within a certain range.
The (![zero-to-one](https://latex.codecogs.com/gif.latex?0%5Crightarrow1) excitation) frequency of the qubit is determined by measuring the qubit response (absorption rate) after each pulse using a Network Analyzer.

This is demonstrated in the figure below.

![Frequency sweep pulse](ibmq/images/img_freq_sweep.png)

3. Once the frequency of the qubit is calibrated, the next step is to determine the strength of a ![pi](https://latex.codecogs.com/gif.latex?%5Cpi) pulse. The latter chages the qubit state from ![](https://latex.codecogs.com/gif.latex?%7C%200%20%5Crangle) to ![](https://latex.codecogs.com/gif.latex?%7C%201%20%5Crangle), and vice versa. This is also called the ![X](https://latex.codecogs.com/gif.latex?X) or ![X180](https://latex.codecogs.com/gif.latex?X180) gate, or bit-flip operator.
A technique called Rabi experiment is used to calibrate the amplitude needed to achieve a ![pi](https://latex.codecogs.com/gif.latex?%5Cpi) rotation from ![](https://latex.codecogs.com/gif.latex?%7C%200%20%5Crangle) to ![](https://latex.codecogs.com/gif.latex?%7C%201%20%5Crangle). The desired rotation is shown on the Bloch sphere in the figure below - you can see that the ![pi](https://latex.codecogs.com/gif.latex?%5Cpi) pulse gets its name from the angle it sweeps over on a Bloch sphere.

![PI Rotation on Bloch sphere](https://github.com/aasfaw/qiskit-intros/blob/master/zero_to_one_X180.png?raw=true")

In the Rabi experiment, a Gaussian pulse schedule is created with fixed duration, sigma and frequency (that was obtained in the previous experiment), and the amplitude is changed in small increments. The qubit response is then measured after each pulse to determine the optimal amplitude.

![Rabi experiment](ibmq/images/img_rabi.png)

4. Similar technique can be used to calibrate and measure the second excited state.
However, due to hardware limitations we cannot apply a strong enough pulse in order to excite the transmon from the ground state to the second excited state directly.
We use the above technique to take the qubit to the first excited state first, and then apply a sideband frequency sweep to find and calibrate the frequency and amplitude needed to take the transmon to the second excited state.

<img src="ibmq/images/img_sideband_freq.png">

5. Once our ![pi](https://latex.codecogs.com/gif.latex?%5Cpi) pulses have been calibrated, we can now create the states ![](https://latex.codecogs.com/gif.latex?%7C%201%20%5Crangle) and ![](https://latex.codecogs.com/gif.latex?%7C2%5Crangle) with good probability.
We can use this to find out what the states ![](https://latex.codecogs.com/gif.latex?%7C%200%20%5Crangle), ![](https://latex.codecogs.com/gif.latex?%7C%201%20%5Crangle) and ![](https://latex.codecogs.com/gif.latex?%7C2%5Crangle) look like in our measurements, by repeatedly preparing them and plotting the measured signal.
The results of the measurements are used to build a discriminator, which is a function which takes a measured and kerneled complex value and classifies it as 0, 1 or 2.

<img src="ibmq/images/img_discriminator.png">

## Executing on IBM Q Backend

We implemented the above experiments using Qiskit Pulse, and executed them on the IBM Q's [ibmq_armonk](https://quantum-computing.ibm.com/services?services=systems) backend.

## Implementing Single-Qutrit Gates

We then used the results from the experiments to construct and test single-qutrit gates on IBM Q's *ibmq_armonk* backend. Below are some examples.

1. **![X01](https://latex.codecogs.com/gif.latex?X%5E%7B%2801%29%7D) gate**

The ![X01](https://latex.codecogs.com/gif.latex?X%5E%7B%2801%29%7D) gate takes qutrit from ![0_state](https://latex.codecogs.com/gif.latex?%7C0%5Crangle) state to ![1_state](https://latex.codecogs.com/gif.latex?%7C1%5Crangle) state and vice versa:

> ![X01_oper](https://latex.codecogs.com/gif.latex?X%5E%7B01%7D%20%7C0%3E%20%3D%20%7C1%3E)

The gate is constructed by sending a Gaussian pulse with the (![zero-to-one](https://latex.codecogs.com/gif.latex?0%5Crightarrow1) excitation) qubit frequency to the qubit's Drive Channel:
```
pulse.play(cal.pulse_rx01(), pulse.DriveChannel(qbit)) #x
```

2. **![X12](https://latex.codecogs.com/gif.latex?X%5E%7B%2812%29%7D) gate**

The ![X12](https://latex.codecogs.com/gif.latex?X%5E%7B%2812%29%7D) gate takes qutrit from ![1_state](https://latex.codecogs.com/gif.latex?%7C1%5Crangle) state to ![2_state](https://latex.codecogs.com/gif.latex?%7C2%5Crangle) state and vice versa:

> ![X12_oper](https://latex.codecogs.com/gif.latex?X%5E%7B12%7D%20%7C1%3E%20%3D%20%7C2%3E)

The gate is constructed by sending a Gaussian pulse with the (![one-to-two](https://latex.codecogs.com/gif.latex?1%5Crightarrow2) excitation) qubit frequency to the qubit's Drive Channel:
```
pulse.play(cal.pulse_rx12(), pulse.DriveChannel(qbit)) #x
```

3. **![Y01](https://latex.codecogs.com/gif.latex?Y%5E%7B%2801%29%7D) gate**

The ![Y01](https://latex.codecogs.com/gif.latex?Y%5E%7B%2801%29%7D) is similar to the ![X01](https://latex.codecogs.com/gif.latex?X%5E%7B%2801%29%7D) gate, except it adds a phase shift.

The gate is constructed by sending three Gaussian pulses with the ((![zero-to-one](https://latex.codecogs.com/gif.latex?0%5Crightarrow1) excitation)) qubit frequency to the qubit's Drive Channel, first with half-amplitude, then the optimal amplitude, then half-amplitude again:
```
yrot_pulse =cal.gaussian_pulse(drive_power=drive_power/2)
pulse.shift_frequency(cal.df01_calib, pulse.DriveChannel(qbit)) #0=>1 freq
pulse.play(yrot_pulse, pulse.DriveChannel(qbit)) #sqrt(y)
pulse.play(cal.pulse_rx01(), pulse.DriveChannel(qbit)) #x
pulse.play(yrot_pulse, pulse.DriveChannel(qbit)) #sqrt(y)
```

The measurement results from running the ![Y01](https://latex.codecogs.com/gif.latex?Y%5E%7B%2801%29%7D) pulse schedule on the *ibmq_armonk* qubit are plotted below. They demonstrate a high fidelity of the gate.

![Y01_gate_plot](ibmq/images/y01_gate_plot.png)


4. **Hadamard ![H02](https://latex.codecogs.com/gif.latex?H%5E%7B%2802%29%7D) gate**

The ![H02](https://latex.codecogs.com/gif.latex?H%5E%7B%2802%29%7D) gate takes qutrit from ![0_state](https://latex.codecogs.com/gif.latex?%7C0%5Crangle) state to a superposition of ![0_state](https://latex.codecogs.com/gif.latex?%7C0%5Crangle) and ![2_state](https://latex.codecogs.com/gif.latex?%7C2%5Crangle):

> ![H02_oper](https://latex.codecogs.com/gif.latex?H%5E%7B01%7D%20%7C0%3E%20%3D%20%5Csqrt%7B1/2%7D%20%28%7C0%3E%20&plus;%20%7C2%3E%29)

The gate is constructed by sending two Gaussian pulses with different frequencies to the qubit's Drive Channel, the first one with ![pi/2](https://latex.codecogs.com/gif.latex?%5Ctheta%20%3D%20%5Cpi/2) and the second one with ![pi](https://latex.codecogs.com/gif.latex?%5Ctheta%20%3D%20%5Cpi):
```
pulse.shift_frequency(cal.df01_calib, pulse.DriveChannel(qbit))
pulse.play(cal.pulse_rx01(theta = np.pi/2), pulse.DriveChannel(qbit)) # PI/2
pulse.shift_frequency(cal.df12_calib, pulse.DriveChannel(qbit))
pulse.play(cal.pulse_rx12(), pulse.DriveChannel(qbit)) # PI
```
The measurement results from running the ![H01](https://latex.codecogs.com/gif.latex?H%5E%7B%2801%29%7D) pulse schedule on the *ibmq_armonk* qubit are plotted below.

![H01_gate_plot](ibmq/images/h01_gate_plot.png)

5. **Hadamard ![H12](https://latex.codecogs.com/gif.latex?H%5E%7B%2812%29%7D) gate**

The ![H12](https://latex.codecogs.com/gif.latex?H%5E%7B%2812%29%7D) gate takes qutrit from ![0_state](https://latex.codecogs.com/gif.latex?%7C0%5Crangle) state to a superposition of ![1_state](https://latex.codecogs.com/gif.latex?%7C1%5Crangle) and ![2_state](https://latex.codecogs.com/gif.latex?%7C2%5Crangle):

> ![1_2_super](https://latex.codecogs.com/gif.latex?H%5E%7B12%7D%20%7C0%3E%20%3D%20%5Csqrt%7B1/2%7D%20%28%7C1%3E%20&plus;%20%7C2%3E%29)

The gate pulse schedule is similar to that of the ![H02](https://latex.codecogs.com/gif.latex?H%5E%7B%2802%29%7D) gate, except the first pulse is sent with ![pi](https://latex.codecogs.com/gif.latex?%5Ctheta%20%3D%20%5Cpi) and the second one with ![pi/2](https://latex.codecogs.com/gif.latex?%5Ctheta%20%3D%20%5Cpi/2):
```
pulse.shift_frequency(cal.df01_calib, pulse.DriveChannel(qbit))
pulse.play(cal.pulse_rx01(), pulse.DriveChannel(qbit)) # PI
pulse.shift_frequency(cal.df12_calib, pulse.DriveChannel(qbit))
pulse.play(cal.pulse_rx12(theta = np.pi/2), pulse.DriveChannel(qbit)) # PI/2
```
The measurement results from running the ![H12](https://latex.codecogs.com/gif.latex?H%5E%7B%2812%29%7D) pulse schedule on the *ibmq_armonk* qubit are plotted below.

![H12_gate_plot](ibmq/images/h12_gate_plot.png)

6. **Equal superposition**

Finally, we constructed and tested a custom gate that takes qutrit from ![0_state](https://latex.codecogs.com/gif.latex?%7C0%5Crangle) state to a superposition of all three states, ![0_state](https://latex.codecogs.com/gif.latex?%7C0%5Crangle), ![1_state](https://latex.codecogs.com/gif.latex?%7C1%5Crangle) and ![2_state](https://latex.codecogs.com/gif.latex?%7C2%5Crangle).
The gate is constructed by sending two Gaussian pulses with different frequencies and different ![theta](https://latex.codecogs.com/gif.latex?%5Ctheta) to the qubit's Drive Channel:
```
theta1 = 2*np.cos(1/np.sqrt(3))
theta2 = np.pi/2
pulse.shift_frequency(cal.df01_calib, pulse.DriveChannel(qbit))
pulse.play(cal.pulse_rx01(theta = theta1), pulse.DriveChannel(qbit))
pulse.shift_frequency(cal.df12_calib, pulse.DriveChannel(qbit))
pulse.play(cal.pulse_rx12(theta = theta2), pulse.DriveChannel(qbit))
```
The measurement results from running the above pulse schedule on the *ibmq_armonk* qubit are plotted below.

![H12_gate_plot](ibmq/images/h123_gate_plot.png)


## Python Code and Jupyter Notebooks

The Python code using Qiskit Pulse can be found in the [ibmq](ibmq) subfolder.

Please review the implementation of the above calibration technique and single-qutrit gates in the [ibmq/class_gates Jupyter notebook](ibmq/class_gates.ipynb).

## References and Further Reading

1. [Front. Phys. **8**, 479 (2019)](www.frontiersin.org/articles/10.3389/fphy.2020.589504/full).
2. [Adv. Quantum Technol. **3**,  1900074 (2020)(https://onlinelibrary.wiley.com/doi/10.1002/qute.201900074)
3. R. V. Krems, Molecules in Electromagnetic Fields: from Ultracold Physics to Controlled Chemistry, Wiley (2018).
4. T. Alexander, N. Kanazawa, D.J. Egger, L. Capelluto, C.J. Wood, A. Javadi-Abhari, D.C.McKay, [Qiskit pulse: programming quantum computers through the cloud with pulses](https://iopscience.iop.org/article/10.1088/2058-9565/aba404)
5. Y. Wang, Z. Hu, B.C. Sanders, S. Kais, [Qudits and High-Dimensional Quantum Computing](https://www.frontiersin.org/articles/10.3389/fphy.2020.589504/full)
6. P. Niemann, R.Wille, R. Drechsler, [Equivalence Checking in Multi-level Quantum Systems](http://www.informatik.uni-bremen.de/agra/doc/konf/14_rc_equivalence_checking_multi-level_quantum_systems.pdf)
7. E.O. Kiktenko, A.K. Fedorov, O.V.Man’ko, V.I.Man’ko, [Multilevel superconducting circuits as two-qubit systems: Operations, state preparation, and entropic inequalities](https://arxiv.org/pdf/1411.0157.pdf)

[Back to README](README.md)
