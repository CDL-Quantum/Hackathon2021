## Business application
![business](./data/business.JPG)

The grid of the future needs to manage the increasing complexity and needs of  electrical power and is at the same time, a key player in the fight against climate change.

We want to optimize the assignment of multiple energy sources (scheduling problem) in the electrical grid such as to 

i) meet the demand,

ii) take into account the costs associated with the switching on and off of the different energy sources 

iii) and the stochastic nature of wind as well as the variability of solar power,  

iii) to find an optimal solution that minimizes the cost of the operation and the cost of carbon emission at the same time. 

To model this problem we use a simplified version of the Unit-Commitment(UC) problem (we don’t take into account maximum voltage per line constraints)  and fit  it into a QUBO formulation which we then solve using the Leap Hybrid Quantum-Classical from D-Wave. We find superior results with Leap compared to the Chimera 
Quantum Annealer and the Simulated Annealear on D-Wave.

## Strategy

We co-optimize the scheduling problem based not only on the cost of the  operation but also on the emission of green house gases. We do so by introducing an additional constraint that penalizes carbon emission. Carbon taxes and Renewable Energy Certificates (RECs) are the two legal tools governments use to enforce the reduction of green house gas emission. Depending on the country either one or both mechanisms are available, the implementation of these tools also vary from country to country.  
In the present model we include the penalization in the form of an extra cost for kwh of fossil sources and we adjusted that cost to the price of RECs in the US. If both carbon taxes and REcs are available an additional optimization could be performed  to assess which combination of both (carbon taxes and RECs)  minimizes the cost of the operation.

## Why did we choose to tackle this problem

This is a NP-hard problem that is a challenge for today’s classical optimization methods.  Increased efficiency gained in solving this problem to higher accuracy. Given the scale of these operations, any improvement, even if small, translates into large savings.

## The Unit Commitment problem

The UC problem pertains to the most challenging class known as NP hard, i.e. we know for sure they can not be solved in polynomial time. 
It is generally
formulated as a large-scale mixed integer nonlinear problem and solving it is very difficult due to
the nonlinear cost function and the combinatorial nature of set of feasible solutions.
Many methods have been proposed in the last decades,  among them heuristic solutions, neural networks, dynamic programming, simulated annealing, to name a few. Some of them might achieve suboptimal solutions,  others may have a slow convergence or a large processing time. UC has been targeted using a quantum annealer and randomly generated instances in 
[ref](https://www.sciencedirect.com/science/article/abs/pii/S0360544219308254), but current limitations of the quantum hardware result in a poor solution for large grids compared to the classical Gurobi solver. A hybrid quantum approach however like the one proposed here, has been proved to give good results for other large-scale mixed-integer programming problems like UC [ref](https://www.sciencedirect.com/science/article/pii/S0098135419307665?casa_token=L41zk8TU[…]hqIHnk9PV3caOSi9TVwQEeONodfuEP4C60SAGp76jm5XPl_cYgIGiRBPh8).




