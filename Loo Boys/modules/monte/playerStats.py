import pandas as pd
import numpy as np
from dimod import BinaryQuadraticModel
from dwave.system import LeapHybridSampler
import matplotlib.pyplot as plt
import warnings
from collections import Counter
import cirq

class playerStata:

    def __init__(self,df):
        self.df = df

    def classical(self):
        iters = []

        for i in range(400):
            td = np.random.normal(0.067, 0.025)*np.random.uniform(300,600)
            iters.append(td)
        
        return iters

    def qMonteCarlo(self):
        iters_q = []

        for i in range(300):
            simulator = cirq.Simulator()
            result = simulator.run(circuit, repetitions=10)
            result = str(result)
            counts = list(Counter(result).items())[2][1]
            
            if counts <= 4:
                td = np.random.normal(0.035, 0.015)*np.random.uniform(300,600)
                iters_q.append(td)
                
            elif (counts > 4) & (counts <= 7):
                td = np.random.normal(0.067, 0.025)*np.random.uniform(300,600)
                iters_q.append(td)
                
            elif counts > 7:
                td = np.random.normal(0.09, 0.015)*np.random.uniform(300,600)
                iters_q.append(td)
        return iters_q

if __name__ == '__main__':
    pass