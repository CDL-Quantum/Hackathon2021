# Xanadu's Challenge Solution Overview

# Description

In this project we are going to solve the Financial Portfolio Optimization problem using qutrits. Portfolio Optimization is the process of choosing the best portfolio out of the set of all portfolios being considered according to some measure like Expected Return or Minimization of Risk. This objective is central in the job of a professional asset manager no matter which financial institution they are working in. For instance, a head of investments in a pension fund, wants to compose their portfolio out of financial instruments that provide stable, low risk returns, so the investors into the pension fund can enjoy a safe financial future. Conversely, a Chief Investment Officer of a hedge fund aims to maximize their quarterly return and maximize their alpha (performance of the fund compared to the benchmark index).  

Financial Optimization problem is a popular topic among people interested in solving Optimization problems on the Quantum Computers. During our time at the Creative Destruction Lab we had pleasure of meeting Román Orús of the Multiverse Computing. He and his company have produces a crucial paper on the topic called "Quantum Portfolio Optimization with Investment Bands and Target Volatility"[1], which provides a technical introduction to the topic. One of the most important results of the paper is the derivation of the Hamiltonian: 

<center>
<img src="images/baseEqn.png">
</center>

When we are picking stocks for our portfolio we have to consider both the asset itself and the time. Effectively, this means that even for one stock we need to consider 365 points. Naturally, when we want to track more companies for a longer time, size of the data for monitoring increases dramatically. This increase in required data makes it computationally expensive to consider an extremely large collection of assets. According to The World Bank there are approximately 43,000 listed companies on the planet [2], if we try monitoring all of them for a year we need to track roughly 16 million data points. For a general discrete probability distribution of n points, we need on classical computer `2 ^ (16 * n)` bits of memory assuming the single precision requirements, a quantum computer made of qubits would need only `16 * n` qubits (from the representational point of view). Amazingly, with a qutrit system we would only need `16 * n / 1.585)` qutrits of memory. In other words n qutrits could represent `1.5 ^ n` times more information than n qubits. We can clearly see then that a qutrit quantum computer is perfectly suited for portfolio optimization problem. 

## Technical Descrption

The problem we are interested in solving is to create an optimal portfolio based on the eqn. (1). For the purposes of our challenge we use data from 60 randomly selected equities in the S&P 500 and use data discrimination techniques to filter out information and restrict our data set sizes since we do not have machines powerful enough to tackle the problem. However, to exploit the representational power of quitrits we employ a large scale [DMRG solver](simple_dmrg.py) to tackle modest optimization sizes. 

In order to achieve this we first have to write out Eq. (1) in a more compact notation using the necessary details of the architecture. To this end we have to use the following expansion of the portfolio weighing operator:
<center>
<img src="images/technical1.png">
</center>
where we utilize N<sub>q</sub> physical bits of local dimension (d = 3), signifying quitrits. We also use N<sub>t</sub> number of time samples and N number of assets (indexed by i). Typically K is used to control the precision or resolution. Here μ(t,i) represents the profit over the incremental time interval. The terms λ(t,i) control the transaction cost and is written in this form to allow time-dependence and asset class dependence. Σ<sup>t</sup><sub>ij</sub> are the terms of the covariance matrix with the diagonal representing the volatility associated with the asset. ϒ controls teh penalty for allowing volatile assets and ρ is the Lagrange multiplier useful to control the constraint to keep the sum of the weighs from exceeding 1.

For purposes of testing our model against real data we use the Density Matrix Renormalization Group (DMRG) and Matrix Product States (MPS) to solve the problem in two steps. The simplest form of Eqn. (1) can be obtained by ignoring transaction costs and volatility. So that the objective reduces to just maximizing the profit while ensuring that the constraint is maintained. To this end we solve a simple problem involving the followign Hamiltonian:

<center>
<img src="images/simpleDMRG.png">
</center>

This compact notation is implemented as Matrix Product Operators (MPOs) in [flatnetwork_simple.py](flatnetwork_simpple.ipynb), which has all the relevant runners etc. to enable computations. 

For our first test we use a portfolio covering 6 quarters, 10 assets and 2 quitrits for precision. The results are shown in the figure below. It is worth mentioning that there are many degenerate states possible and the formulation does not always guarantee that the constraint will be obeyed. In a real setting we would explore the full parameter space, which in the interest of time we did not pursue here.

<table align="center">
    <tr>
        <td>
            <img src="images/simpleDMRGbigsys1.png">
        </td>
        <td>
            <img src="images/simpleDMRGbigsys2.png">
        </td>        
    </tr>
</table>

We next tackle the full problem using the same dataset but now the Hamiltonian is a lot more complicated, as shown below:

<center>
<img src="./images/fullDMRG.png">
</center>

This has been implemented as Matrix Product Operators (MPOs) in [flatnetwork.py](flatnetwork_simpple.ipynb), which has all the relevant runners etc. to enable computations. We plot the optimum solutions below the parameters of which can be found along with all the relevant data in the file [dataloader_test.ipynb](dataloader_test.ipynb)

<table align="center">
    <tr>
        <td>
            <img src="images/DMRGbigsys1.png">
        </td>
        <td>
            <img src="images/DMRGbigsys2.png">
        </td>        
    </tr>
</table>

Unfortunately, even modest sizes like these cannot be simulated on the simulators and current hardware. Additionally, since the simulation tools available are restricted to qubits we further loose out on expressibility, which in our case manifests as loss of precision in characterizing the weights and therefore yield suboptimal solutions. Nonetheless for completeness and demonstration purposes we port over to Xanadu's Pennylane simulation package where we solve simpler versions of this problem using QAOA, which is a native algorithm intended for quantum hardware. These computations are done using only two quarters and two assets with representation on two qubits. For the purposes of comparsion we also undertake DMRG simulations.

Once again using our datasorting techniques we obtain a variety of clustered data we pick the two most viable options and proceed to run computations (shown below).

<table align="center">
    <tr>
        <td>
            <img src="images/img1.png">
        </td>
        <td>
            <img src="images/img2.png">
        </td>        
    </tr>
</table>

The DMRG solutions are optimally constrained in this case as shown below. 
<table align="center">
    <tr>
        <td>
            <img src="images/img3.png">
        </td>
        <td>
            <img src="images/img4.png">
        </td>        
    </tr>
</table>

For the purposes of QAOA we have to once again conver the Hamiltonian from the operator representation to the Pauli representation. The file [PennylaneQAOA.ipynb](./PennylaneQAOA.ipynb) contains all the conversions needed to be able to do this. As per the edict of QAOA, we setup the cost Hamiltonian as well as the mixer Hamiltonian and assign 2 layers of them with 2 parameters per layer, which are then optimized. In the end of 400 steps the probabiloty associated with the different basis states are shown below.
<center>
    <img src="./images/QAOA1.png" width=400>
</center>
The solutions found by QAOA do not match the optimal soluions of DMRG, but we haven't fine tuned our schedule. However, our framework can easil show this can be done.
<table align="center">
    <tr>
        <td>
            <img src="images/img6.png">
        </td>
        <td>
            <img src="images/img7.png">
        </td>        
    </tr>
</table>

## Python Code and Jupyter Notebooks

- [Data for both the 2008 Financial Crisis and the 2020 COVID-19 Pandemic](https://github.com/olegxtend/Hackathon2021/tree/main/CosmiQ/xanadu/data) 
- [Dataloader class for Data preprocessing](https://github.com/olegxtend/Hackathon2021/blob/main/CosmiQ/xanadu/dataloader_class.py)
- [Python Implementation of the Flat Network](https://github.com/olegxtend/Hackathon2021/blob/main/CosmiQ/xanadu/flatnetwork.py)
- [Using DMRG to solve the Financial Portfolio Optimization Problem](https://github.com/olegxtend/Hackathon2021/blob/main/CosmiQ/xanadu/simple_dmrg.py)
- [Using PennyLane QAOA to solve the Financial Portfolio Optimization Problem](https://github.com/olegxtend/Hackathon2021/blob/main/CosmiQ/xanadu/PennylaneQAOA.ipynb)


## References

1. [Samuel Palmer, Serkan Sahin, Rodrigo Hernandez, Samuel Mugel, and Roman Orus "Quantum Portfolio Optimization with Investment Bands and Target Volatility"](https://arxiv.org/abs/2106.06735)

2. [The World Bank Data on the Number of the Total Listed Companies](https://data.worldbank.org/indicator/CM.MKT.LDOM.NO)

[Back to README](README.md)
