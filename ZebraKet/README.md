<p align="center">
  <img  height="200" src="./resources/ZebraKet%20Banner.png">
</p>

## Project Description 
We show how an online grocer will optimize between two objectives: 
1) selection on least number of suppliers provding all required inventory 
2) maximizing inventory profit. 

We also provide a novel approach to solving competing supply-chain objectives through our Chained Optimization Rules Engine&reg; CORE&reg; method. This allows one to arbitrarily chain qubos together and solve complex optimization problems via multiple simple qubos.

## Setup
1. Make sure you have Anaconda installed and configured.
2. conda env create -f environment.yml
    
Original environment creation steps (only do this if step 2 did not work): 
```
conda create -n zebraket-cdl-hackathon-2021 python=3.9
source activate zebraket-cdl-hackathon-2021
conda install --name zebraket-cdl-hackathon-2021 ipykernel -y
conda install --name zebraket-cdl-hackathon-2021 pylint -y
conda install pandas==1.3.0
pip install dwave-ocean-sdk
```

## How to Use

#### We recommend you checkout our notebooks in [./notebooks](./notebooks/README.md) with detailed information about our code. 


## Challenges Solved

- Objective 1: We want to limit the number of suppliers based on the set of items they provide. This pre-selection was formulated into the "set cover" problem.

<p align="center">
  <img  height="200" src="./resources/equation1.png">
</p>

We convert this formulation into a binary quadratic model (BQM) and solve using D-Wave's Hybrid Solver with a small, medium and large dataset.  We then solve our "real" dataset.

- Objective 2: We want to maximize the overall profit by selecting an optimal set of inventory from the chosen suppliers while staying within our budget. This profit maximization is performed using the Knapsack formulation.

<p align="center">
  <img  height="200" src="./resources/equation2.png">
</p>

We develop a QUBO formulation of this using Andrew Lucas's formula[1].  However, we use our own Lagrange terms. We solve this also on a small, medium and large dataset.  We also then solve our "real" dataset.


- Summary of Results

Results for objective 1: Suppliers (QTY & List of Suppliers)

<p align="center">
  <img  height="200" src="./resources/datatable1.png">
</p>


Results for objective 2: Inventory Profit (Total Profit Potential, Inventory)

<p align="center">
  <img  height="220" src="./resources/datatable2.png">
</p>

## Project Details: 
  - Further walkthrough of what you did 

  The overall scope of our project was to show that multiple objectives can be handled together through a process of chaining and that gives comparable results to solving both objectives together.

  The diagram below shows the overall objectives and process. Detailed account of the formulae, QUBO and execution along with results are in the jupyter notebooks.  
  
<p align="center">
  <img  height="700" src="./resources/equation3.png">
</p>

The detailed explanation of the business motivation, importance of this use case and applicability to other industries and similar competing objectives is described in the business applications document.

For more details refer to the [Business Application](./Business_Application.md)

  - Links to any Jupyter notebooks/scripts
  - Link to Presentation

## Contributors 
Alex Khan, Theo Cleland, Ehsan Torabizadeh, Ziwei Qiu

## References
[1] Lucas, A., 2014. Ising formulations of many NP problems. Frontiers in physics, 2, p.5.
