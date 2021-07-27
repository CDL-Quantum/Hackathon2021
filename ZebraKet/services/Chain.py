class Chain(list):
    def __init__(self) -> None:
        super().__init__()
    
    def process_single_qubo(self, index, sampler, **kwargs):
        qubo = self[index]
        qubo.solve(sampler, **kwargs)
    
    def process_best(self):
        """Processes the chain but only passes the best solutions forward
        """

        previous_qubo = None
        for qubo in self:
            if previous_qubo is None: 
                # first qubo to process
                qubo.solve()
                previous_qubo = qubo
                continue
            next_iteration_data = previous_qubo.post_process[0]
            print('Starting next iteration with data', next_iteration_data)
            qubo.build(**next_iteration_data)
            qubo.solve()
            previous_qubo = qubo
        

if __name__ == "__main__":

    from models.ProfitQubo import ProfitQubo
    from utils.data import read_profit_optimization_data
    from config import standard_mock_data
    # from neal import SimulatedAnnealingSampler
    from dwave.system import LeapHybridDQMSampler

    budget = 1000
    max_number_of_products = 30
    
    profit, cost = read_profit_optimization_data(standard_mock_data['small'])
    sampler1 = LeapHybridDQMSampler().sample_dqm
    sampler2 = LeapHybridDQMSampler().sample_dqm
    
    qubo0 = ProfitQubo(sampler1, profit, cost)
    qubo0.define_post_process_function(lambda solution, energy: dict(profits=profit, costs=cost))
    # qubo0.solve()
    # print(qubo0.post_process)
    
    qubo1 = ProfitQubo(sampler2)

    chain = Chain()
    chain.append(qubo0)
    chain.append(qubo1)

    chain.process_best()
