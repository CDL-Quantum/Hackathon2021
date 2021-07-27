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
        elements_df = pd.DataFrame(json['elements'])
        elements_types_df = pd.DataFrame(json['element_types'])
        teams_df = pd.DataFrame(json['teams'])
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
    def __init__(self,data_url) -> None:
        self.df_mid, self.df_gk, self.df_def, self.df_fwd = getDataFrames(url)

    def set_up_bqm(self,df1, percent, max_weight):
        df1['value_season'] = df1['value_season'].astype(float)
        values = list(df1['value_season'])
        weights = list(df1['now_cost'])
        volumes = [x/x for x in range(1, len(values))]

        n = len(values)
        variables = list(range(n))
        weight = max_weight*percent

        return variables, values, volumes
    
    def bqm_position(variables, values, volumes, max_volume):
        bqm = BinaryQuadraticModel('BINARY')

        variables = [bqm.add_variable(v, -values[v]) for v in variables]
        
        slacks_volume = bqm.add_linear_equality_constraint(
        [(x, v) for x, v in zip(variables, volumes)],
        constant=-max_volume,
        lagrange_multiplier=500
        )

        return bqm
        

class getPlayers:
    def __init__(self,url,token) -> None:
        self.sBQM = soccerBQM(url)
        self.variables_def, self.values_def, self.volumes_def = self.sBQM.set_up_bqm(self.sBQM.df_def, 20, 1000)
        self.variables_mid, self.values_mid, self.volumes_mid = self.sBQM.set_up_bqm(self.sBQM.df_mid, 30, 1000)
        self.variables_fwd, self.values_fwd, self.volumes_fwd = self.sBQM.set_up_bqm(self.sBQM.df_fwd, 30, 1000)
        self.variables_gk, self.values_gk, self.volumes_gk = self.sBQM.set_up_bqm(self.sBQM.df_gk, 20, 1000)
        bqm_mid=bqm_position(self.variables_mid,self.values_mid,self.volumes_mid, 3)
        bqm_fwd=bqm_position(self.variables_fwd,self.values_fwd,self.volumes_fwd, 1)
        bqm_gk=bqm_position(self.variables_gk,self.values_gk,self.volumes_gk, 0)
        bqm_def=bqm_position(self.variables_def,self.values_def,self.volumes_def, 3)
        self.token = token 
        
    def get_players(bqm, df):
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

ans = getPayers("KmJQ-eb7dea9880650063660800305a6750d9fe70bb21")