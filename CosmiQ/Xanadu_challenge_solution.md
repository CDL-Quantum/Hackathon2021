# Xanadu's Challenge Solution Overview

# Introduction

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




## Business Proposal
<p align = center>
<img src="./images/wall_street.jpg" height="200">
</p>
  
In our work we have proposed a solution to the well known optimization problem using the most recent development in the field of quantum computing. The business potential for this technology is extraordinary in the field of finance. Qutrits have the ability to represent `1.5 ^ n` times more information than `n` qubits, which will be a crucial difference maker for the portfolio optimization. Currently, the price for running a single task on the quantum computer is around 30 cents. While this might not seem like a lot, we need to understand that if an entire department is using a quantum computer to calculate complex simulations the costs increase exponentially. 

In 2019, Top ten asset managers have more than 30 trillion assets under management[3] and are in a continuous competition with each other to increase their market share. While quantum computing for finance is still in the nascent stages of development, there is an strong interest on behalf of the asset managers in quantum technologies. For instance, companies like J.P. Morgan Chase & Co. and Goldman Sachs have dedicated division for the development of the quantum algorithms for the NISQ devices. 

Potential suitors for this technology would include asset management companies specializing in highly diversified mutual funds. For example, Vanguard Total Stock Market Index Fund Admiral Shares[4], was created in 1992 and includes entirety of the US equity market, which amounts to more than 3,600 stocks ranging from small to large cap growth and value stocks. The company that operates this fund, Vanguard, would develop a natural interest in the qutrit quantum computers, because using them will allow for tracking over the larger periods of time. Additionally, qutrit quantum computers will also dramaticallly decrease the computation costs of optimization because qutrits are exponentially more efficient than both the bits and qubits.

Additionally, we can also consider a use case where an investment manager holds on to the same group of assets for an extremely long time. This could be an international financial regulatory institution like the International Monetary Fund and the World Bank or a large credit rating agency like Standard & Poors or Moody's. For instance, IMF can look at the group of treasury bonds from several sovereign nations and evaluate which one of these countries has the most favorable investment climate. Standard & Poors made the most popular index fund in the US today - S&P 500. Rating agencies continuosly update their ratings to reflect the most accurate financial state of a given asset. While, it is true credit agencies rely heavily on the fundamental analysis and close reading of the accounting statements, it is important to point out that technical analysis is becoming an attractive option for these entities because of it's efficiency. 

## Python Code and Jupyter Notebooks

- [Data for both the 2008 Financial Crisis and the 2020 COVID-19 Pandemic](https://github.com/olegxtend/Hackathon2021/tree/main/CosmiQ/xanadu/data) 
- [Dataloader class for Data preprocessing](https://github.com/olegxtend/Hackathon2021/blob/main/CosmiQ/xanadu/dataloader_class.py)
- [Python Implementation of the Flat Network](https://github.com/olegxtend/Hackathon2021/blob/main/CosmiQ/xanadu/flatnetwork.py)
- [Using DMRG to solve the Financial Portfolio Optimization Problem](https://github.com/olegxtend/Hackathon2021/blob/main/CosmiQ/xanadu/simple_dmrg.py)
- [Using PennyLane QAOA to solve the Financial Portfolio Optimization Problem](https://github.com/olegxtend/Hackathon2021/blob/main/CosmiQ/xanadu/PennylaneQAOA.ipynb)
- [Using Strawberry Fields QAOA to solve the Financial Portfolio Optimization Problem](https://github.com/olegxtend/Hackathon2021/blob/main/CosmiQ/xanadu/StrawberryFields.ipynb)

## References

1. [Samuel Palmer, Serkan Sahin, Rodrigo Hernandez, Samuel Mugel, and Roman Orus "Quantum Portfolio Optimization with Investment Bands and Target Volatility"](https://arxiv.org/abs/2106.06735)
2. [The World Bank Data on the Number of the Total Listed Companies](https://data.worldbank.org/indicator/CM.MKT.LDOM.NO)
3. [Top 10 Asset Management Firms in the World](https://www.statista.com/statistics/431790/leading-asset-management-companies-worldwide-by-assets/)
4. [Vanguard Total Stock Market Index Fund Admiral Shares](https://www.nasdaq.com/market-activity/funds-and-etfs/vtsax)

[Back to README](README.md)
