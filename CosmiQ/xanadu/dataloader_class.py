import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class data_loader():
    def __init__(self,filename):
        df = pd.read_csv(filename)
        df = df.drop_duplicates()
        df = df.groupby('Symbol')['PRICECLOSE'].apply(list)
        self.asset_names = list(df.keys())
        self.asset_values = np.concatenate([np.expand_dims(np.array(a),axis=1) for a in df.values],axis=1)
        self.num_assets = self.asset_values.shape[1]
        self.time_stamp = self.asset_values.shape[0]
    
    def split_windows(self,days_per_period):
        n_win=int((self.time_stamp-self.time_stamp%days_per_period)/days_per_period)
        values_window = np.reshape(self.asset_values[:n_win*days_per_period,:],(days_per_period,n_win,self.num_assets))
        self.num_windows = n_win
        self.mus = np.log(values_window[1:,:,:]/values_window[:-1,:,:])
        
    def filter_assets(self,num_assets=20,method='random'):
        num_assets = min(num_assets,self.num_assets)
        if method == 'random':
            inds = np.random.choice(self.num_assets, num_assets, replace=False)
        elif method =='relevant':
            inds = np.where(np.sum(self.return_mut()>0,axis=0)>0)            
            inds=inds[0][:min(num_assets,len(inds[0]))]
        
        self.asset_values = self.asset_values[:,inds]
        self.mus = self.mus[:,:,inds]
        self.num_assets = len(inds)
    
    def return_mut(self):
        mut = np.mean(self.mus,axis=0)
        return mut
    
    def return_sigmat(self):
        sigmat = np.matmul(np.transpose(self.mus,[1,2,0]),np.transpose(self.mus,[1,0,2]))
        return sigmat
    
    def return_stdt(self):
        stdt = np.std(self.mus,axis=0)
        return stdt
    
    def plot_trajectories(self):
        plt.plot(self.return_stdt(),self.return_mut(),'o-');
        plt.ylabel('profit')
        plt.xlabel('volatility')
