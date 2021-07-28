import pandas as pd
import numpy as np
from dimod import BinaryQuadraticModel
from dwave.system import LeapHybridSampler
import matplotlib.pyplot as plt
import warnings
from collections import Counter
import cirq


class teamResults:

    def __init__(self,df) -> None:
        self.df = df
    
    def classical(self):
        sim = {}

        for j in range(100):

            games = []

            for i in range(len(self.df)):
                if self.df['VisitorPPG'][i] > 0.8*np.exp(np.random.rand(1))*self.df['HomePPG'][i]:
                    games.append(self.df['Visitor'][i])
                else:
                    games.append(self.df['Home'][i])
                    
                cts = Counter(games)
                sim[j] = list(cts.items())
        tms = {}

        for i in range(100):
            for j in sim[i]:
                try:
                    tms[j[0]].append(j[1])
                    
                except:
                    tms[j[0]] = [j[1]]
        return tms
    
    def quantum(self):
        qubit = cirq.GridQubit(0, 0)
        circuit = cirq.Circuit(
            cirq.X(qubit)**0.5,  
            cirq.measure(qubit, key='m')  
        )
        lst = []
        for i in range(100):
            simulator = cirq.Simulator()
            result = simulator.run(circuit, repetitions=5)
            lst.append(result)

        dicts ={}
        for i in lst:
            try:
                dicts[str(i)].append(1)
            except:
                dicts[str(i)] = [1]
        return dicts

if __name__ == '__main__':
    pass