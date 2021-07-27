# QuTrits

While the majority of quantum algorithms are based on qbits, 2-level systems with the ![](https://latex.codecogs.com/gif.latex?%7C%200%20%5Crangle%20%3D%20%5B0%2C1%5D) and ![](https://latex.codecogs.com/gif.latex?%7C%201%20%5Crangle%20%3D%20%5B1%2C0%5D). 
The majority of gate operations can be categorized into single-qbit gates, and two-qbits gates; for example, the *Pauli-X* rotates the state ![](https://latex.codecogs.com/gif.latex?%7C%201%20%5Crangle) to ![](https://latex.codecogs.com/gif.latex?%7C%200%20%5Crangle); ![](https://latex.codecogs.com/gif.latex?X%20%7C%201%20%5Crangle%20%3D%20%7C%200%20%5Crangle).

As it was pointed in Ref. [1], quantum compting could also be done using multi-level quantum systems (**qudits**) as the building block in quantum information. 
Why bother using qudits? It has been theoretically illustrated that qudits can store and processes information more efficienlty than using qubits Ref. [2]. 
The following natural arising question is how to engeneer qudits?, for example cold molecules in ultra cold temepratures have non-degenerate states  under the present of an external electric field (Stark shift) Ref. [3].
None the less, it will be ideal to desing qudtis taking advantage of the current architectures, for example, superconducting quantum processors.

Qutrits are qudits constructed from quantum states like spin-1 systems, where the basis is ![](https://latex.codecogs.com/gif.latex?%7C0%5Crangle%2C%7C1%5Crangle) and ![](https://latex.codecogs.com/gif.latex?%7C2%5Crangle). 
In order to have a unviversal quantum computer based on qutris we are required to have a well defined set of ternary quantum gates.
For example, the ***X*** and the **Z** gates are,

![X qtrits gates](https://latex.codecogs.com/gif.latex?X%5E%7B%2801%29%7D%20%3D%20%5Cbegin%7Bpmatrix%7D%200%20%26%201%20%26%200%20%5C%5C%201%20%26%200%20%26%200%5C%5C%200%20%26%200%20%26%201%20%5Cend%7Bpmatrix%7D%20%5C%3B%5C%3B%5C%3B%20X%5E%7B%2802%29%7D%20%3D%20%5Cbegin%7Bpmatrix%7D%200%20%26%200%20%26%201%20%5C%5C%200%20%26%201%20%26%200%5C%5C%201%20%26%200%20%26%200%20%5Cend%7Bpmatrix%7D%5C%3B%5C%3B%5C%3B%20X%5E%7B%2812%29%7D%20%3D%20%5Cbegin%7Bpmatrix%7D%201%20%26%200%20%26%200%20%5C%5C%200%20%26%200%20%26%201%20%5C%5C%200%20%26%201%20%26%200%20%5Cend%7Bpmatrix%7D)

![Z Qtrits gates](https://latex.codecogs.com/gif.latex?%5Csmall%20Z%5E%7B%280%29%7D%20%3D%20%5Ctext%7Bdiag%7D%20%5C%7B-1%20%5C%3B1%5C%3B1%5C%7D%20%5C%3B%5C%3B%20Z%5E%7B%281%29%7D%20%3D%20%5Ctext%7Bdiag%7D%20%5C%7B1-1%5C%3B%5C%3B1%5C%7D%5C%3B%5C%3B%20Z%5E%7B%282%29%7D%20%3D%20%5Ctext%7Bdiag%7D%20%5C%7B%201%5C%3B%5C1%5C%3B-1%5C%7D)

For the **Z** gates, all gates are diagonal matrices (*diag*). The Hamadard gates are, 

![](https://latex.codecogs.com/gif.latex?%5Csmall%20H%5E%7B%2801%29%7D%20%3D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%7D%7D%5Cbegin%7Bpmatrix%7D%201%20%26%201%20%26%200%20%5C%5C%20-1%20%26%201%20%26%200%5C%5C%200%20%26%200%20%26%20%5Csqrt%7B2%7D%20%5Cend%7Bpmatrix%7D%20%5C%3B%5C%3B%5C%3BH%5E%7B%2802%29%7D%20%3D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%7D%7D%5Cbegin%7Bpmatrix%7D%201%20%26%200%20%26%201%20%5C%5C%201%20%26%20%5Csqrt%7B2%7D%20%26%200%5C%5C%201%20%26%200%20%26%20-1%20%5Cend%7Bpmatrix%7D%20%5C%3B%5C%3B%5C%3B%20X%5E%7B%2812%29%7D%20%3D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%7D%7D%5Cbegin%7Bpmatrix%7D%20%5Csqrt%7B2%7D%20%26%200%20%26%200%20%5C%5C%200%20%26%201%20%26%201%20%5C%5C%200%20%26%20-1%20%26%201%20%5Cend%7Bpmatrix%7D)


The second main component for a universal quantum computer with qutrits are two-qutrits gates. The  **CNOT** gate, commonly used in to entagle two qubits, has the following form for qutrits, 



# Rerences
1. [Front. Phys. **8**, 479 (2019)](www.frontiersin.org/articles/10.3389/fphy.2020.589504/full).
2. [Adv. Quantum Technol. **3**,  1900074 (2020)](https://onlinelibrary.wiley.com/doi/10.1002/qute.201900074)
3. R. V. Krems, Molecules in Electromagnetic Fields: from Ultracold Physics to Controlled Chemistry, Wiley (2018).      