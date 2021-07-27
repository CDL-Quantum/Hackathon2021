# Class to manage data (for example, loading data from csv, generating mock data etc)
from math import prod
import pandas as pd
import numpy as np
import random
import os
import time
from config import data_dir, missing_product_price

def generate_mock_data(number_products: int=10, number_suppliers:int=10, price_save_name=None, cost_save_name=None, markup: float=2.4):
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
        C = np.zeros((number_suppliers, number_products)) + missing_product_price
        #cost of all items for every supplier
        for i in range (number_products):
            #base cost used to calculate the cost of the item at each supplier
            c_base = random.random()*25
            for s in range (number_suppliers):
                # There will be a 25% chance that a given supplier does not have a product 
                if random.random() > 0.25:
                    #Cost of item fluctuates from c_base 
                    C[s, i] = random.randint(90,130) / 100 * c_base
        
        df = pd.DataFrame(C, index=[f'supplier{i}' for i in range(number_suppliers)], columns=[f'item{i}' for i in range(number_products)])
        return df
        
    def generate_mock_price_data(cost_dataframe: pd.DataFrame, markup: float):
        """Generates fake data for cost of products per supplier as a pandas table where rows are suppliers and columns are products
        
        This uses the cost_dataframe generated from "generate_mock_cost_data" and marks the price up by multiplying by markup
        """
        cost = np.array(cost_dataframe)
        cost[cost==missing_product_price] = np.inf  # Make missing prices infinite so that we can easily calculate the min cost
        min_cost = np.amin(cost, axis=0) 
        profit = [c*markup for c in min_cost]
        df = pd.DataFrame([profit, min_cost], columns=cost_dataframe.columns, index=['price', 'cost'])
        return df

    cost_df = generate_mock_cost_data(number_products=number_products, number_suppliers=number_suppliers)
    price_df = generate_mock_price_data(cost_dataframe=cost_df, markup=markup)

    default_save_name = f'-n_products_{number_products}-n_suppliers_{number_suppliers}-{time.strftime("%Y%m%d-%H%M%S")}.csv'
    price_filename = f'price{default_save_name}' if price_save_name is None else price_save_name
    cost_filename = f'cost{default_save_name}' if cost_save_name is None else cost_save_name

    cost_data_dir = os.path.join(data_dir, cost_filename)
    price_data_dir = os.path.join(data_dir, price_filename)

    if not os.path.isdir(data_dir):
        print(f'Creating data directory: {data_dir}')
        os.makedirs(data_dir)

    print(f'Saving cost data to {cost_data_dir}')
    print(f'Saving price data to {price_data_dir}')

    cost_df.to_csv(cost_data_dir)
    price_df.to_csv(price_data_dir)

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

def read_inventory_optimization_data(cost_file:str) -> tuple[list, list[set]]: 
    """Reads cost csv (from generate_mock_data) and converts it into a tuple suitable for use in the supplier optimization formulation

    Params:
    str cost_file -- filepath to the cost matrix

    Returns:
    list of products (our inventory),
    list of sets of products (each set is the inventory of a particular supplier)
    """
    cost_df = pd.read_csv(cost_file, index_col=0)
    cost_np = np.array(cost_df)
    product_names = cost_df.columns
    supplier_names = cost_df.index
    
    supplier_inventories = []
    for supplier_idx in range(len(supplier_names)):
        idx_in_stock = np.where(cost_np[supplier_idx] != missing_product_price)
        supplier_inventories.append(set([product_names[idx] for idx in idx_in_stock[0]]))

    return product_names, supplier_inventories

def read_profit_optimization_data(cost_file:str, price_file:str) -> tuple[list[float], list[float]]:
    """Reads cost and price csv files to return data suitable to be ingested in the profit optimization formulation
    
    Params (both files can be generated by generate_mock_data):
    str cost_file -- filepath to the cost matrix
    str price_file -- filepath to the price matrix

    Returns
    List of floats indicating the cost per item
    List of floats indicating the profit per item
    """
    price_df = pd.read_csv(price_file, index_col=0)
    pass


if __name__ == "__main__":

    # # Example usage creating data
    # cost_dataframe, price_dataframe = generate_mock_data(20, 10)
    # print('Cost DataFrame:\n', cost_dataframe, '\n')

    # print('Price DataFrame:\n', price_dataframe, '\n')

    # from config import standard_mock_data
    # p1 = pd.read_csv(standard_mock_data['small']['price'], index_col=0)
    # print(p1)

    # # Example usage reading data for the inventory problem
    inventory, supplier_inventories = read_inventory_optimization_data('data/small-cost-mock.csv')
    print('\nMy desired inventory', inventory)
    print('\n\nSupplier inventories', supplier_inventories)