from abc import ABC, abstractmethod

class AbstractQubo(ABC):
    def __init__(self, sampler) -> None:
        super().__init__()
        self.sampler = sampler
        self.solution_set = None
        self.energy_set = None
        self.response = None

    def solve(self, **kwargs):
        """Solves the qubo using the passed in sampler
        """
        self.response = self.sampler(self.qubo, **kwargs)
        print('\n\nresponse: ')
        print(self.response)
        self.solution_set = self.response.record.sample
        self.energy_set = self.response.record.energy

    @property
    @abstractmethod
    def qubo(self):
        pass

    @property
    def post_process(self, *args):
        print(self._post_process)
        print(self._post_process([1,2,3], 29))
        return self._post_process(*args)

    @post_process.setter
    def post_process(self, fn):
        """Called after self.solve is called and this passes data into the next qubo

        fn -- generic function that will be called in Chain.py and returns **kwargs for the next qubo in the chain
        """
        self._post_process = fn

    @abstractmethod
    def lazy_init(self):
        pass