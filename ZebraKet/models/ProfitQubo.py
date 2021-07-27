from math import log2, floor
from dimod import DiscreteQuadraticModel
import numpy as np
from models.AbstractQubo import AbstractQubo

class ProfitQubo(AbstractQubo):
    def __init__(self, profits=None, costs=None, budget: float=100, max_number_of_products=10) -> None:
        """Initializes the ProfitQubo
        
        profits (list):
            List of profits associated with the items
            If None, you must call self.build() before calling self.solve()
        costs (list):
            List of costs associated with the items
            If None, you must call self.build() before calling self.solve()
        budget (int):
            Maximum allowable cost
        max_number_of_products(int):
            Maximum allowable products for each product
        """
        super().__init__()
        self.profits = profits
        self.costs = costs
        self.budget = budget
        self.max_number_of_products = max_number_of_products + 1 # also take into account the value 0
        if profits is not None and costs is not None: 
            self.build(profits, costs)

    def build(self, profits: list[float], costs: list[float]): 
        """Bulds the qubo

        Args: 
        profits - list of profits we can get per product
        costs - list of costs per product
        """
        print(f'Building QUBO')
        self.profits = np.array(profits)
        self.costs = np.array(costs)
        self.qubo = self.construct_dqm()
    
    def construct_dqm(self):
        """Construct DQM for the generalized knapsack problem
        Args:
            
        Returns:
            Discrete quadratic model instance
        """

        pieces = range(self.max_number_of_products)
        
        # First guess the lagrange
        lagrange = max(self.profits)*0.2

        # Number of objects
        x_size = len(self.profits)

        # Lucas's algorithm introduces additional slack variables to
        # handle the inequality. M+1 binary slack variables are needed to
        # represent the sum using a set of powers of 2.
        M = floor(log2(self.budget))
        num_slack_variables = M + 1

        # Slack variable list for Lucas's algorithm. The last variable has
        # a special value because it terminates the sequence.
        y = [2**n for n in range(M)]
        y.append(self.budget + 1 - 2**M)
        
        ##@  Discrete Quadratic Model @##
        dqm = DiscreteQuadraticModel()
        
        #@ Add variables @##
        for k in range(x_size):
            dqm.add_variable(self.max_number_of_products, label='x' + str(k))

        for k in range(num_slack_variables):
            dqm.add_variable(2, label='y' + str(k)) # either 0 or 1

        ##@ Hamiltonian xi-xi terms ##
        for k in range(x_size):
            dqm.set_linear('x' + str(k), lagrange * (self.costs[k]**2) * (np.array(pieces)**2) - self.profits[k]*pieces)


        # # Hamiltonian xi-xj terms
        for i in range(x_size):
            for j in range(i + 1, x_size):
                biases_dict = {}
                for piece1 in pieces:
                    for piece2 in pieces:
                        biases_dict[(piece1, piece2)]=(2 * lagrange * self.costs[i] * self.costs[j])*piece1*piece2

                dqm.set_quadratic('x' + str(i), 'x' + str(j), biases_dict)

        # Hamiltonian y-y terms
        for k in range(num_slack_variables):
            dqm.set_linear('y' + str(k), lagrange*np.array([0,1])* (y[k]**2))

        # Hamiltonian yi-yj terms 
        for i in range(num_slack_variables):
            for j in range(i + 1, num_slack_variables): 
                dqm.set_quadratic('y' + str(i), 'y' + str(j), {(1,1):2 * lagrange * y[i] * y[j]})

        # Hamiltonian x-y terms
        for i in range(x_size):
            for j in range(num_slack_variables):
                biases_dict = {}
                for piece1 in pieces:
                    biases_dict[(piece1, 1)]=-2 * lagrange * self.costs[i] * y[j]*piece1

                dqm.set_quadratic('x' + str(i), 'y' + str(j), biases_dict) 
        
        return dqm

if __name__ == "__main__":

    from dwave.system import LeapHybridDQMSampler
    from neal import SimulatedAnnealingSampler
    
    prices = [3.5, 3.4, 3.8, 6.1]
    costs = [1.5, 1.4, 1.8, 2.1]
    profits = [p - c for p, c in zip(prices, costs)]
    
    # qubo = ProfitQubo(LeapHybridDQMSampler().sample_dqm, profits=profits, costs=costs, budget=100, max_number_of_products=20)
    # qubo.solve()

    # sampler = SimulatedAnnealingSampler().sample_dqm

    sampler = LeapHybridDQMSampler().sample_dqm

    qubo = ProfitQubo(profits=profits, costs=costs, budget=100, max_number_of_products=20)
    qubo.solve(sampler)
    print(qubo.response)