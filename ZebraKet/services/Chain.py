class Chain(list):
    def __init__(self) -> None:
        super().__init__()
    
    def process_single_qubo(self, index, sampler, **kwargs):
        qubo = self[index]
        qubo.solve(sampler, **kwargs)
    
    def process_best(self):
        """Processes the chain but only passes the best solutions forward
        """
        print(self)

        previous_qubo = None
        for qubo in self:
            if previous_qubo is None: 
                # first qubo to process
                qubo.solve()
                previous_qubo = qubo
                continue
            qubo.lazy_init(**previous_qubo.post_process)
            qubo.solve()
            

        # for index, qubo_instance in enumerate(self):
        #     if index == 0:
        #         qubo = qubo_instance.lazy_init()




    # def process_chain(self):


    

if __name__ == "__main__":

    from models.ProfitQubo import ProfitQubo, PrototypeProfitQubo
    from utils.data import read_profit_optimization_data
    from config import standard_mock_data
    # from neal import SimulatedAnnealingSampler
    from dwave.system import LeapHybridDQMSampler

    budget = 1000
    max_number_of_products = 30
    
    profit, cost = read_profit_optimization_data(standard_mock_data['small'])
    qubo1 = PrototypeProfitQubo(LeapHybridDQMSampler().sample_dqm, budget, max_number_of_products)
    qubo1.lazy_init(profit, cost)
    qubo1.post_process = lambda solution, energy: dict(
        profits = solution, 
        costs = energy
    )

    print(qubo1.post_process([1, 2, 3], 100))

    # # qubo1.solve()
    # # print(qubo1.solution_set)

    # qubo2 = PrototypeProfitQubo(LeapHybridDQMSampler().sample_dqm, budget, max_number_of_products)
    # # qubo1.lazy_init(profit, cost)
    # # qubo1.post_process = lambda solution_set, energy_set: [0, 0, 0], [0, 0, 0]




    # # qubo2 = PrototyProfitQubo(budget, max_number_of_products)




    # # qubo1 = ProfitQubo(profits=profit, costs=cost, budget=budget, max_number_of_products=max_number_of_products)
    # # sampler = LeapHybridDQMSampler().sample_dqm
    # # qubo.solve(sampler, **{"num_reads":100, "num_sweeps": 100000})
    # # print(qubo.solution_set)

    # # qubo1.solution_set.samples()[0]





    # chain = Chain()
    # chain.append(qubo1)
    # chain.append(qubo2)

    # chain.process_best()