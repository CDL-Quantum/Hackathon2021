# Class to manage data (for example, loading data from csv, generating mock data etc)
import pandas as pd
import numpy as np
import random
import os
import time
from config import save_dir

def generate_mock_data(number_products: int=10, number_suppliers:int=10, save_name=None, markup: float=2.4):
    """Generates 2 dataframes for cost per supplier and price per item

    Input Paramaters: 
    int number_products -- Number of products to mock
    int number_suppliers -- Number of suppliers to mock
    float markup -- Amount of markup for each item (used when calculating the price)
    
    Returns: 
    Cost Dataframe (rows = suppliers, columns = products)
    Price Dataframe (rows = ['price'], columns = products)
    """
    def generate_mock_cost_data(number_products: int=10, number_suppliers:int=10):
        """Generates fake data for cost of products per supplier as a pandas table where rows are suppliers and columns are products
        """
        # Cost Matrix
        # random.seed(a=1, version=2)
        C = np.zeros((number_suppliers, number_products))
        #cost of all items for every supplier
        for i in range (number_products):
            #base cost used to calculate the cost of the item at each supplier
            c_base = random.random()*25
            for s in range (number_suppliers):
                #Cost of item fluctuates from c_base 
                C[s, i] = random.randint(90,130) / 100 * c_base
        
        df = pd.DataFrame(C, index=[f'supplier{i}' for i in range(number_suppliers)], columns=[f'item{i}' for i in range(number_products)])
        return df
        
    def generate_mock_price_data(cost_dataframe: pd.DataFrame, markup: float):
        """Generates fake data for cost of products per supplier as a pandas table where rows are suppliers and columns are products
        
        This uses the cost_dataframe generated from "generate_mock_cost_data" and marks the price up by multiplying by markup
        """
        cost = np.array(cost_dataframe)
        P = np.amax(cost, axis=0) 
        P = [p*markup for p in P]
        df = pd.DataFrame([P], columns=cost_dataframe.columns, index=['price'])
        return df

    cost_df = generate_mock_cost_data(number_products=number_products, number_suppliers=number_suppliers)
    price_df = generate_mock_price_data(cost_dataframe=cost_df, markup=markup)
    save_name = save_name if save_name is not None else f'-n_products_{number_products}-n_suppliers_{number_suppliers}-{time.strftime("%Y%m%d-%H%M%S")}.csv'

    cost_save_dir = os.path.join(save_dir, f'cost{save_name}')
    price_save_dir = os.path.join(save_dir, f'price{save_name}')

    if not os.path.isdir(save_dir):
        print(f'Creating data directory: {save_dir}')
        os.makedirs(save_dir)

    print(f'Saving cost data to {cost_save_dir}')
    print(f'Saving price data to {price_save_dir}')

    cost_df.to_csv(cost_save_dir)
    price_df.to_csv(price_save_dir)

    return cost_df, price_df

def parse_profit_dataframe(data: pd.DataFrame) -> list[list[str], list[float], list[float]]:
    """Creates the profit dataframe

    Keyword arguments:
    data -- DataFrame containing profit and cost for each product. There must be a "profit" row and "cost" row in the dataframe
    
    Returns:
    Tuple of product names (str)
    Tuple of product cost (float)
    Tuple of product profit (price - cost) (float)

    Example input: 

            | apples | bananas 
    price   | 6.5    | 7.1
    cost    | 2.5    | 2.4
    """
    cost = list(data.loc['cost']) 
    price = list(data.loc['price'])
    profit = [p - c for p, c in zip(price, cost)]
    return list(data), cost, profit

if __name__ == "__main__":

    # Example usage

    cost_dataframe, price_dataframe = generate_mock_data(20, 10)
    print('Cost DataFrame:\n', cost_dataframe, '\n')

    print('Price DataFrame:\n', price_dataframe, '\n')