from dimod import BinaryQuadraticModel, BINARY
import numpy as np
from models.Qubo import Qubo

class SupplierQubo(Qubo):
    # Lagrange multipliers A>B>0
    lagrange_a = 2
    lagrange_b = 1

    def __init__(self, inventory: list[int or str], supplier_inventory: list[set[int or str]]) -> None:
        """Initializes the SupplierQubo
        
        inventory (list):
            List of items we want for our inventory
        supplier_inventory (list of sets):
            List for each supplier their inventory
        """
        super().__init__()
        self.inventory = inventory
        self.supplier_inventory = supplier_inventory
        # Create indicator variables
        self.indicators = []
        for i in range(len(self.supplier_inventory)):
            self.indicators.append([1 if self.inventory[a] in self.supplier_inventory[i] else 0 for a in range(len(self.inventory))])

        self.qubo = self.construct_bqm()

    def construct_bqm(self):
        """Construct BQM for the generalized set cover problem
        Args:
            
        Returns:
            Binary quadratic model instance
        """

        ##@  Binary Quadratic Model @##
        bqm = BinaryQuadraticModel(BINARY)

        # Add linear terms
        # x linear terms
        x = [bqm.add_variable(f'x_{i+1}', SupplierQubo.lagrange_a*sum(self.indicators[i])+SupplierQubo.lagrange_b) for i in range(0,len(self.supplier_inventory))]
        # print('x variables:',x)

        # y_am linear terms
        y = []
        for a in range(1,len(self.inventory)+1):
            y.append([bqm.add_variable(f'y_{a,m}', SupplierQubo.lagrange_a*(m**2-1)) for m in range(1,len(self.supplier_inventory)+1)])
        # print('y variables:',y)

        # Add quadratic terms

        # x_i-x_j terms
        for i in range(1,len(self.supplier_inventory)+1):
            for j in range(i+1,len(self.supplier_inventory)+1):
                key = ('x_' + str(i), 'x_' + str(j))
                bqm.quadratic[key] = 2*SupplierQubo.lagrange_a*np.dot(np.array(self.indicators[i-1]),np.array(self.indicators[j-1]))
                
        # y_am - y_an terms
        for m in range(1,len(self.supplier_inventory)+1):
            for n in range(m+1,len(self.supplier_inventory)+1):
                for a in range(1,len(self.inventory)+1):
                    key = ('y_('+str(a)+', '+str(m)+')', 'y_('+str(a)+', '+str(n)+')')
                    bqm.quadratic[key] = 2*SupplierQubo.lagrange_a*(1+m*n)
                    
        # x_i-y_am terms
        for i in range(1,len(self.supplier_inventory)+1):
            for m in range(1,len(self.supplier_inventory)+1):
                for a in range(1,len(self.inventory)+1):
                    key = ('x_' + str(i), 'y_('+str(a)+', '+str(m)+')')
                    bqm.quadratic[key] = -2*SupplierQubo.lagrange_a*m*self.indicators[i-1][a-1]
        
        return bqm

if __name__ == "__main__":

    # from dimod import ExactSolver
    from neal import SimulatedAnnealingSampler
   
    # Define a simple set cover problem
    # U = list(set(np.random.randint(10, size=(5))))
    U = list(set([1,2,4]))

    # V = [set(np.random.randint(10, size=(5))) for i in range(5)]
    V = [set([1]),set([1,2]),set([4]), set([2])]
    
    qubo = SupplierQubo(U, V)
    qubo.solve(SimulatedAnnealingSampler().sample, **{"num_reads":100, "num_sweeps": 100000})
    print(qubo.solution_set)