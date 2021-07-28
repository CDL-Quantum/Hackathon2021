import requests
import pandas as pd
import numpy as np
from dimod import BinaryQuadraticModel
from dwave.system import LeapHybridSampler

def getDataFrames(url):
    try:
        r = requests.get(url)
    except Exception as e:
        raise(e)
    _json = r.json()
    df_mid=df_gk=df_def=df_fwd = None 
    if _json:
        elements_df = pd.DataFrame(_json['elements'])
        elements_types_df = pd.DataFrame(_json['element_types'])
        teams_df = pd.DataFrame(_json['teams'])
        slim_elements_df = elements_df[['second_name','team','element_type','selected_by_percent','now_cost','minutes','transfers_in','value_season','total_points']]
        df = slim_elements_df.merge(elements_types_df, left_on = 'element_type', right_on = 'id')
        df = df[['plural_name_short','second_name','team','element_type','selected_by_percent','now_cost','minutes','transfers_in','value_season','total_points']]
        df = df[df.minutes > 100]
        df.loc[df.plural_name_short == 'GKP', 'class'] = 1
        df.loc[df.plural_name_short == 'DEF', 'class'] = 2
        df.loc[df.plural_name_short == 'FWD', 'class'] = 3
        df.loc[df.plural_name_short == 'MID', 'class'] = 4
        df_mid = df[df.plural_name_short == 'MID']
        df_gk = df[df.plural_name_short == 'GKP']
        df_def = df[df.plural_name_short == 'DEF']
        df_fwd = df[df.plural_name_short == 'FWD']
    return df_mid, df_gk, df_def, df_fwd

class soccerBQM:
    '''Class for determining the best starting 11 for a paticular team
    '''
    def __init__(self,data_url,token,limit,fromation=[4,4,2]) -> None:
        '''
        Inputs: data_url(String)--> the fantasy football url where the data is kept 
                token(String)--> Token for Dwave to be able to run this code
                limit(Int)--> This is is the max amount of money spent 
                formation[List[Int]]--> list of integers which denote the players fromation [#_def,#_mid,#_fwd]
        '''
        if sum(fromation) !=10:
            raise(Exception('sum of fromation must be 10'))
        self.df_mid, self.df_gk, self.df_def, self.df_fwd = getDataFrames(data_url)
        self.variables_def, self.values_def, self.volumes_def = self.set_up_bqm(self.df_def, 20)
        self.variables_mid, self.values_mid, self.volumes_mid = self.set_up_bqm(self.df_mid, 30)
        self.variables_fwd, self.values_fwd, self.volumes_fwd = self.set_up_bqm(self.df_fwd, 30)
        self.variables_gk, self.values_gk, self.volumes_gk = self.set_up_bqm(self.df_gk, 20)
        # there can and must always be only one goalkeeper
        self.bqm_gk=self.bqm_position(self.variables_gk,self.values_gk,self.volumes_gk, 0)
        self.bqm_def=self.bqm_position(self.variables_def,self.values_def,self.volumes_def, fromation[0]-1)
        self.bqm_mid=self.bqm_position(self.variables_mid,self.values_mid,self.volumes_mid, fromation[1]-1)
        self.bqm_fwd=self.bqm_position(self.variables_fwd,self.values_fwd,self.volumes_fwd, fromation[2]-1)
        # Other Variables
        self.token = token 
        self.max_weight = limit

    def set_up_bqm(self,df1, percent):
        #TODO allow for precentages
        ''' This function does all the prework for the BQM

        Input: df1(DataFrame)--> this is a pandas dataframe that stores the data
               percent(int)--> the percentage of the budget you would like to allocate to the position
        Output: variables(List)-->list of the qubits form 0->n-1
                values(List)-->list of all the values for each player
                volumes(List)--> a list of 1s with len(n)
        '''
        df1['value_season'] = df1['value_season'].astype(float)
        values = list(df1['value_season'])
        weights = list(df1['now_cost'])
        volumes = [x/x for x in range(1, len(values))]

        n = len(values)
        variables = list(range(n))
        weight = self.max_weight*percent

        return variables, values, volumes
    
    def bqm_position(variables, values, volumes, max_volume):
        '''
        Input:  variables(List)-->list of the qubits form 0->n-1
                values(List)-->list of all the values for each player
                volumes(List)--> a list of 1s with len(n)
        Output: bqm(BinaryQuadraticModel)-->BinaryQuadraticModel for a given position
        '''
        bqm = BinaryQuadraticModel('BINARY')

        variables = [bqm.add_variable(v, -values[v]) for v in variables]
        
        slacks_volume = bqm.add_linear_equality_constraint(
        [(x, v) for x, v in zip(variables, volumes)],
        constant=-max_volume,
        lagrange_multiplier=500
        )

        return bqm

    def get_players(self,bqm, df):
        '''
        Input: bqm(BinaryQuadraticModel)-->BinaryQuadraticModel for a given position
                df(DataFrame)-->A pandas dataframe with all the players
        Output: DataFrame --> a dataframe of all the players chosen for this position
        '''
        sampler = LeapHybridSampler(token = self.token)
        response = sampler.sample(
            bqm, time_limit=25,
            )
        best_solution = response.first.sample
        indices = []

        for i, v in best_solution.items():
            if v != 0:
                indices.append(i)

        return df.iloc[indices][['second_name','plural_name_short' ]]
    
    def find_team(self):
        ''' 
        Input: None
        Output: None, prints the team and the players
        '''
        print('The following is the best team that was determined based on your inputs')
        print()
        print('The Keeper is')
        print(self.get_players(self.bqm_gk, self.df_gk))
        print()
        print('The defender/s are')
        print(self.get_players(self.bqm_def, self.df_def))
        print()
        print('The midfeilder/s are')
        print(self.get_players(self.bqm_mid, self.df_mid))
        print()
        print('The forward/s are')
        print(self.get_players(self.bqm_fwd, self.df_fwd))

if __name__ == '__main__':
    print('This is an example run with the formation=[4,4,2]')
    data_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    token = "KmJQ-eb7dea9880650063660800305a6750d9fe70bb21"
    limit = 1000
    soccer_bqm = soccerBQM(data_url,token,limit)
    soccer_bqm.find_team()