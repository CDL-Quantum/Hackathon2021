from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pennylane as qml
import sklearn.datasets
import sklearn.decomposition
import torch
import os
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

### Defining helper functions ###
#TODO allow for different headings
def weightFunc(row):
    '''
    Calculates the weights of a row in a dataframe
    '''
    return row['Won'] - row['Lost'] + row['Draw']*0.5 +row['GF']*.25 - row['A']*.25

def whoWon(score):
    '''
    Input : score(String)-->a string that is the score ex. '4-1'
    Output: return 1 if home team won 0 otherwise. If draw chose randomly
    '''
    v_list = score.split(' - ')
    if v_list[0] == v_list[1]:
        return np.random.randint(0, 1)
    if v_list[0] > v_list[1]:
        return 1
    else:
        return 0

def getTeamWeights(path):
    '''
    Input: path(String)-->the path to the data
    Output: dataframe with the data transformed as needed
    '''
    df = pd.read_csv(path)
    df['Weight'] =df.apply (lambda row: weightFunc(row),axis=1)
    df = df[['Team','Weight']]
    df = df.replace('Manchester City', value ='Man City')
    df = df.replace('Leicester City',value ='Leicester')
    df = df.replace('Sheffield United',value ='Sheffield Utd')
    df = df.replace('Norwich City',value ='Norwich')
    df = df.replace('Wolverhampton Wanderers',value ='Wolves')
    df = df.replace('West Ham United',value ='West Ham')
    df = df.replace('Tottenham Hotspur',value ='Spurs')
    df = df.replace('Newcastle United',value ='Newcastle')
    df = df.replace('Manchester United',value ='Man Utd')
    df = df.replace('Brighton and Hove Albion',value ='Brighton')
    return df

def getData(path,df):
    df_matches = pd.read_csv(path)
    df_matches = df_matches[['Home Team','Away Team','Result']]
    df_matches['y'] = df_matches['Result'].apply (lambda value: whoWon(value))
    teams = df_matches['Home Team'].unique()
    for team in teams:
        index = df.index
        cond = df['Team'] == team
        i = index[cond].tolist()[0]
        df_matches = df_matches.replace(team,df['Weight'][i])
    df_matches['x'] = df_matches[['Home Team', 'Away Team']].values.tolist()
    df_matches = df_matches[['x','y']]
    x = df_matches['x'].values.tolist()
    y = df_matches['y'].values.tolist()
    return x,y

class predictScores:
    '''
    A class for predicting the scores of a match
    '''

    def __init__(self,n_wires,n_features,n_classes,params,n_samples,dev) -> None:
        '''
        Inputs: n_wires(Int)-->number of qubits in the circuit
                devs(qml.devices)--> the device that you want to use

        '''
        self.n_wires = n_wires
        self.n_features = n_features
        self.n_classes = n_classes
        self.n_samples = n_samples
        self.qnodes = qml.QNodeCollection([qml.QNode(self.circuit1, dev, interface="torch")])
        self.params = params
    
    def circuit1(self, x=None):
        for i in range(self.n_wires):
            qml.RX(x[i % self.n_features], wires=i)
            qml.Rot(*self.params[0, i], wires=i)

        qml.CZ(wires=[0, 1])
        qml.CZ(wires=[1, 2])

        for i in range(self.n_wires):
            qml.Rot(*self.params[1, i], wires=i)
        return qml.expval(qml.PauliZ(0)), qml.expval(qml.PauliZ(1))
    
    def decision(self,softmax):
        return int(torch.argmax(softmax))


    def predict_point(self,x_point=None, parallel=True):
        results = self.qnodes(self.params, x=x_point, parallel=False)
        softmax = torch.nn.functional.softmax(results, dim=1)
        choice = torch.where(softmax == torch.max(softmax))[0][0]
        chosen_softmax = softmax[choice]
        return self.decision(chosen_softmax), self.decision(self.softmax[0]), int(choice)

    def predict(self, x=None, parallel=True):
        predictions_ensemble = []
        predictions_0 = []
        choices = []

        for i, x_point in enumerate(x):
            if i % 10 == 0 and i > 0:
                print("Completed up to iteration {}".format(i))
            results = self.predict_point(self.params, x_point=x_point, parallel=parallel)
            predictions_ensemble.append(results[0])
            predictions_0.append(results[1])
            choices.append(results[2])

        return predictions_ensemble, predictions_0, choices


if __name__ == '__main__':
    print("Starting process")
    #constant
    n_features = 2
    n_classes = 2
    n_samples = 380
    n_wires = 3

    path = os.path.abspath(os.path.join( "../data/", 'prem_table_2020.csv'))
    p2 = os.path.abspath(os.path.join( "../data/", 'epl-2019-GMTStandardTime.csv'))
    df = getTeamWeights(path)
    x,y = getData(p2,df)
    split = int(n_samples*0.90)
    x_train = x[:split]
    x_test = x[split:]
    y_train = y[:split]
    y_test = y[split:]

    params = np.array(qml.init.strong_ent_layers_normal(n_layers=3, n_wires=3))
    dev = qml.device("qiskit.aer", wires=n_wires)

    europ = os.path.abspath(os.path.join( "../data/", 'euroGroupStage.csv'))
    df_Euro = d.read_csv(europ)
    df_Euro.columns = ['Team','Won','Draw','Lost','GF','A']
    df_Euro['Weight'] =df_Euro.apply (lambda row: weightFunc(row),axis=1)
    df_Euro =  df_Euro[['Team','Weight']]

    ro16p = os.path.abspath(os.path.join( "../data/", 'euroGroupStage.csv'))
    df_ro16 = pd.read_csv(ro16p)   
    x_ro16 = df_ro16['x'].values.tolist()
    x_ro16 = [list(map(float ,x.split(','))) for x in x_ro16]

    
    euroScores = predictScores(n_wires,n_features,n_classes,params,n_samples,dev)
    print("Predicting on training dataset")
    p_train, p_train_0,  choices_train = predictScores.predict(params, x=x_train)
    print("Predicting on Euro Test")
    p_test, p_test_0, choices_test = predictScores.predict(params, x=x_ro16)