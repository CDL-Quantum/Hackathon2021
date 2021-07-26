from dimod import BinaryQuadraticModel
import numpy as np
from models.Qubo import Qubo

class SupplierQubo(Qubo):
    # Lagrange multipliers A>B>0
    lagrange_a = 2
    lagrange_b = 1

    def __init__(self, profits: list[float], costs: list[float], budget: float, max_number_of_products=10) -> None:
        """Initializes the SupplierQubo
        
        profits (array-like):
            Array of profits associated with the items
        costs (array-like):
            Array of costs associated with the items
        budget (int):
            Maximum allowable cost
        max_number_of_products(int):
            Maximum allowable products for each product
        """
        super().__init__()
        self.profits = np.array(profits)
        self.costs = np.array(costs)
        self.budget = budget
        self.max_number_of_products = max_number_of_products + 1 # also take into account the value 0
        self.qubo = self.construct_dqm()

    def construct_dqm(self):
        """Construct BQM for the generalized set cover problem
        Args:
            
        Returns:
            Binary quadratic model instance
        """

        ##@  Binary Quadratic Model @##
        bqm = BinaryQuadraticModel('BINARY')

        # Add linear terms
        # x linear terms
        x = [bqm.add_variable(f'x_{i+1}', SupplierQubo.lagrange_a*sum(I[i])+SupplierQubo.lagrange_b) for i in range(0,len(V))]
        print('x variables:',x)

        # y_am linear terms
        y = []
        for a in range(1,len(U)+1):
            y.append([bqm.add_variable(f'y_{a,m}', A*(m**2-1)) for m in range(1,len(V)+1)])
        print('y variables:',y)

        # Add quadratic terms

        # x_i-x_j terms
        for i in range(1,len(V)+1):
            for j in range(i+1,len(V)+1):
                key = ('x_' + str(i), 'x_' + str(j))
                bqm.quadratic[key] = 2*A*np.dot(np.array(I[i-1]),np.array(I[j-1]))
                
        # y_am - y_an terms
        for m in range(1,len(V)+1):
            for n in range(m+1,len(V)+1):
                for a in range(1,len(U)+1):
                    key = ('y_('+str(a)+', '+str(m)+')', 'y_('+str(a)+', '+str(n)+')')
                    bqm.quadratic[key] = 2*A*(1+m*n)
                    
        # x_i-y_am terms
        for i in range(1,len(V)+1):
            for m in range(1,len(V)+1):
                for a in range(1,len(U)+1):
                    key = ('x_' + str(i), 'y_('+str(a)+', '+str(m)+')')
                    bqm.quadratic[key] = -2*A*m*I[i-1][a-1]
        
        return bqm

if __name__ == "__main__":

    from dimod import ExactSolver
    
    prices = [3.5, 3.4, 3.8, 6.1]
    costs = [1.5, 1.4, 1.8, 2.1]
    profits = [p - c for p, c in zip(prices, costs)]
    
    qubo = ProfitQubo(profits=profits, costs=costs, budget=100, max_number_of_products=20)
    qubo.solve(LeapHybridDQMSampler().sample_dqm)

    # for k in range(x_size):
    #         dqm.set_linear('x' + str(k), lagrange * (costs[k]**2) * (np.array(pieces)**2) - profits[k]*pieces)