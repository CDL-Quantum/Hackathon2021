from abc import ABC, abstractmethod

class AbstractQubo(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.solution_set = None
        self.energy_set = None
        self.response = None
        self.qubo = None

    @abstractmethod
    def build(self):
        pass

    def solve(self, sampler, **kwargs):
        """Solves the qubo using the passed in sampler and arguments
        """
        print('Solving Qubo')
        if self.qubo is None:
            raise ValueError('Qubo has not been built. Please call .build()')
        self.response = sampler(self.qubo, **kwargs)
        # HACK - for supplier qubo.... 
        hack_post_process = getattr(self, "_post_process", None)
        if hack_post_process:
            self.solution_set = hack_post_process(self.response.samples())
        else:
            self.solution_set = self.response.record.sample
        self.energy_set = self.response.record.energy

        print('Solved')
        print(self.response)

    def define_post_process_function(self, fn):
        self.post_process_function = fn

    @property
    def post_process(self):
        return [self.post_process_function(solution, energy) for solution, energy in zip(self.solution_set, self.energy_set)]
