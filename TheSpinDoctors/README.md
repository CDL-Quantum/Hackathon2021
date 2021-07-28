# Green Optimization on a Quantum Annealer
### A cost-efficient optimization of energy networks to reduce carbon emissions

![sunset](./data/sunset.jpg)

Global climate change is the biggest challenge of our era, and a vital issue for electrical energy distributors.
Today, energy grid distribution focuses on optimizing for lowest operating costs, leaving consumers to offset their CO2 emission with different methods, like carbon trading credits.

**Green Optimization** is the solution to this problem. By co-optimizing for 
reduced CO2 emissions and operational costs we help Transmission System Operators go green and save money at the same time.

Our solution provides a prototype to solve UC in a Green Optimization framework by using **Quantum Annealing**. 
We call this problem the **Green Unit Commitment problem** (GUC).

## Structure: where to look for the implementation
The main optimization is based on using the D-Wave Leap Hybrid solver. 
Explanation of the mapping of the problem to a QUBO problem and the 
implementation are presented in [this notebook](./Green_optimization_QuantumAnnealing.ipynb).

An extension with more realistic scenarios and a larger
energy network is provided [here](./Green_optimization_QuantumAnnealing_XL.ipynb). 

Finally, an alternative implementation with a smaller scale problem
has been performed with the QAOA algorithm, both on the Rigetti PyQuil 
([see here for Rigetti](./Green_optimization_QuantumAnnealing_QAOA_Rigetti.ipynb)) and the IBM Qiskit frameworks 
([see here for IBM](./Green_optimization_QuantumAnnealing_QAOA_IBM.ipynb)).

## Requirements
Make sure the modules in the requirements.txt are installed:

`$ pip install -r requirements.txt` 

Note: to run the codes and the notebooks, please set 
the '[TheSpinDoctors](./TheSpinDoctors/)' folder as project folder. 


For running the IBM implementation we suggest to import the notebook
in the [IBM Quantum Lab](https://quantum-computing.ibm.com/).

## Challenge We Solved
**D-Wave Challenge**:

Practical applications require domain knowledge and solutions that work at a real-world scale. Hybrid development brings the power of quantum to the scale of classical. Users are challenged to select a practical problem and to solve it at scale with Leap's hybrid solvers (BQM and DQM hybrid solvers).

As a hint, problems with graph structure like the maximum independent set, structural imbalance, and maximum cut can be translated to a binary quadratic model without additional variables and problems like graph coloring and clustering can be efficiently mapped to the discrete quadratic model.

Check out https://cloud.dwavesys.com/leap/examples/ for ideas, but use your creativity! The best projects would be the ones that solve the most practical problems.

**Note**: Refer to the Bootcamp training for ideas on how to use the most recent Ocean features.

## Project Details: 

Optimization models have been widely used in the electric power industry to solve the unit commitment problem (UC), the process of scheduling and dispatching electric power generation resources.
UC is considered an NP-hard problem, and an active field of research. The inclusion of renewable energies into the system poses an additional challenge.
Deterministic, meta-heuristic and combinatorial approaches, from deep learning to 
non-linear programming and simulated annealing have been applied with different degrees of success.

**Our solution provides a prototype to solve UC in a Green Optimization framework by using Quantum Annealing.** 

We call this problem the **Green Unit Commitment problem** (GUC).

GUC can be formulated as a (multi-objective) QUBO problem, amenable to be solved on a quantum computer, with a cost function expressing the trade-off between:
- **Operational costs**: usage, maintenance, fuel and on-off related costs
- **Carbon emission costs**: proxied by price of Renewable Energy Certificates or carbon taxes

We define the variables related to the activity of a given energy source at a given time in the schedule.
Thus, the trade-off cost vs carbon emission can easily be implemented in QUBO. 
For details on the implementation please check the  [Green optimization notebook](./Green_optimization_QuantumAnnealing.ipynb).

We optimize the GUC on the D-Wave Leap Hybrid Solver to find solutions that maximize the revenue while minimizing the carbon emission. 
Alternative quantum and classical implementations have been performed to test the performance of the solver. 
These include Simulated Annealing (D-Wave), Quantum Annealing (D-Wave) and QAOA (Rigetti SDK).
For the QAOA implementation, we provide two notebooks (linked in the [main notebook](./Green_optimization_QuantumAnnealing.ipynb)) 
with:
- implementation of QAOA in [Rigetti PyQuil framework](./Green_optimization_QuantumAnnealing_QAOA_Rigetti.ipynb))
- implementation of QAOA in [IBM Qiskit frameworks](./Green_optimization_QuantumAnnealing_QAOA_IBM.ipynb)).

Finally, an extension with more realistic scenarios and a larger
energy network is provided in [this](./Green_optimization_QuantumAnnealing_XL.ipynb) notebook. 

## Business application and presentation

Please find:
- [here the Business Presentation](./presentation.pdf)
- and here [additional information on the Business application](./Business_Application.md)

## Contributors 
All authors equally contributed to the project and they are listed in alphabetic order:

- **Matthew Bishara**: background in computational high energy physics, works now on energy industry MIP optimization problems applying quantum computing, machine learning, and classical computing methods. 
- **Giuseppe Colucci**: PhD in physics, works in the Banking industry for 7 years, expert in financial modelling, strategic hedging and optimization techniques.
- **Oscar Fanelli**: Italian pizza-lover, "born" as software engineer 13 years ago, founded and grew a start-up as CTO, now working as Head of Engineering, focusing on product, processes and people management. 
- **Felipe Ferreira de Freitas**: researcher working on applications in collider
phenomenology and gravitational waves detection, with main expertise is in deep learning and
computer vision techniques applied to particle physics.
- **Johanna Fuks**: quantum physicist working in academia (University of Buenos Aires, Argentina) seeking for new challenges and connections. 
  Interested in finding a common language between quantum chemistry, solid-state physics
and quantum information/computing.
