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

For running the IBM implementation we suggest to import the notebook
in the [IBM Quantum Lab](https://quantum-computing.ibm.com/).

## Challenge We Solved
**D-Wave Challenge**:

Practical applications require domain knowledge and solutions that work at a real-world scale. Hybrid development brings the power of quantum to the scale of classical. Users are challenged to select a practical problem and to solve it at scale with Leap's hybrid solvers (BQM and DQM hybrid solvers).

As a hint, problems with graph structure like the maximum independent set, structural imbalance, and maximum cut can be translated to a binary quadratic model without additional variables and problems like graph coloring and clustering can be efficiently mapped to the discrete quadratic model.

Check out https://cloud.dwavesys.com/leap/examples/ for ideas, but use your creativity! The best projects would be the ones that solve the most practical problems.

**Note**: Refer to the Bootcamp training for ideas on how to use the most recent Ocean features.
## Project Details: 
  - Further walkthrough of what you did 
  - Links to any Jupyter notebooks/scripts
  - Business applications
  - Link to Presentation

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
