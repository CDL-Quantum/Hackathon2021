import pandas as pd
import numpy as np
from dimod import BinaryQuadraticModel
from dwave.system import LeapHybridSampler

class draftPlayers:

    def __init__(self,df) -> None:
        self.df = df
        self.lst_qb = list(df[df.FantPos == 'QB'].index)
        self.values = list(df['FantPt'])
        self.weights = list(df['dollar_value'])
        self.volumes = [x/x for x in range(1, len(self.values))]

        n = len(self.values)
        self.variables = list(range(n))

    def doDraft(self):
        bqm = BinaryQuadraticModel('BINARY')

        variables = [bqm.add_variable(v, -self.values[v]) for v in self.variables]

        slacks_volume = bqm.add_linear_equality_constraint(
        [(x, v) for x, v in zip(variables, self.volumes)],
        constant=-15,
        lagrange_multiplier=400
        )

        slacks_volume = bqm.add_linear_equality_constraint(
        [(x, 1) for x in variables if x in self.lst_qb],
        constant=-1,
        lagrange_multiplier=100
        )


        slacks_weight = bqm.add_linear_inequality_constraint(
        [(x, v) for x, v in zip(variables, self.weights)],
        constant=-75,
        lagrange_multiplier=600,
        label = 'weight')
        sampler = LeapHybridSampler(token = "KmJQ-eb7dea9880650063660800305a6750d9fe70bb21")
        response = sampler.sample(
            bqm, time_limit=25,
            )
        best_solution = response.first.sample

        indices = []

        for i, v in best_solution.items():
            if not str(i).startswith('s'):
                if v != 0:
                    indices.append(i)
        return pd.DataFrame(self.df.iloc[indices][['Player','Pick', 'FantPos', 'dollar_value' ]])

if __name__ == '__main__':
    pass