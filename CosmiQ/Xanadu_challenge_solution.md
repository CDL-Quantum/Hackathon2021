# Xanadu's Challenge Solution Overview

# Description

In this project we are going to solve the Financial Portfolio Optimization problem using qutrits. Portfolio Optimization is the process of choosing the best portfolio out of the set of all portfolios being considered according to some measure like Expected Return or Minimization of Risk. This objective is central in the job of a professional asset manager no matter which financial institution they are working in. For instance, a head of investments in a pension fund, wants to compose their portfolio out of financial instruments that provide stable, low risk returns, so the investors into the pension fund can enjoy a safe financial future. Conversely, a Chief Investment Officer of a hedge fund aims to maximize their quarterly return and maximize their alpha (performance of the fund compared to the benchmark index).  

Financial Optimization problem is a popular topic among people interested in solving Optimization problems on the Quantum Computers. During our time at the Creative Destruction Lab we had pleasure of meeting Román Orús of the Multiverse Computing. He and his company have produces a crucial paper on the topic called "Quantum Portfolio Optimization with Investment Bands and Target Volatility"[1], which provides a technical introduction to the topic. One of the most important results of the paper is the derivation of the Hamiltonian: 

> ![Hamiltonian](https://latex.codecogs.com/svg.image?H=-%5Cmu%5E%7BT%7D%20%5Comega&plus;%5Cfrac%7B%5Cgamma%7D%7B2%7D%20%5Comega%5E%7BT%7D%20%5CSigma%20%5Comega&plus;%5Crho%5Cleft(%5Csum_%7Bn%7D%20%5Comega_%7Bn%7D-1%5Cright)%5E%7B2%7D)

When we are picking stocks for our portfolio we have to consider both the asset itself and the time. Effectively, this means that even for one stock we need to consider 365 points. Naturally, when we want to track more companies for a longer time, size of the data for monitoring increases dramatically. This increase in required data makes it computationally expensive to consider an extremely large collection of assets. According to The World Bank there are approximately 43,000 listed companies on the planet [2], if we try monitoring all of them for a year we need to track roughly 16 million data points. For a general discrete probability distribution of n points, we need on classical computer `2 ^ (16 * n)` bits of memory assuming the single precision requirements, a quantum computer made of qubits would need only `16 * n` qubits (from the representational point of view). Amazingly, with a qutrit system we would only need `16 * n / 1.585)` qutrits of memory. In other words n qutrits could represent 1.5 ^ n times more information than n qubits. We can clearly see then that a qutrit quantum computer is perfectly suited for portfolio optimization problem. 

## Python Code and Jupyter Notebooks


The Python code for the Xanadu's challenge can be found in the [xanadu](xanadu) subfolder.


## References

1. [Samuel Palmer, Serkan Sahin, Rodrigo Hernandez, Samuel Mugel, and Roman Orus "Quantum Portfolio Optimization with Investment Bands and Target Volatility"](https://arxiv.org/abs/2106.06735)

2. [The World Bank Data on the Number of the Total Listed Companies](https://data.worldbank.org/indicator/CM.MKT.LDOM.NO)

[Back to README](README.md)
