from abc import ABC

class AbstractQubo(ABC):
    def solve(self, sampler, **kwargs):
        """Solves the qubo using the passed in sampler
        """
        response = sampler(self.qubo, **kwargs)
        self.solution_set = response.record.sample
        self.energy_set = response.record.energy