# Class to manage data (for example, loading data from csv, generating mock data etc)
import pandas as pd
import numpy as np
import random

def generate_mock_cost_data(number_products: int=10, number_suppliers:int=10):
    """Generates fake data for cost of products per supplier as a pandas table where rows are suppliers and columns are products
    """
    # Cost Matrix
    # random.seed(a=1, version=2)
    C = np.zeros((number_suppliers, number_products))
    #cost of all items for every supplier
    for i in range (number_products):
        #base cost used to calculate the cost of the item at each supplier
        c_base = random.random()*1000
        for s in range (number_suppliers):
            #Cost of item fluctuates from c_base 
            C[s, i] = random.randint(90,130) / 100 * c_base
    
    df = pd.DataFrame(C, index=[f'supplier{i}' for i in range(number_suppliers)], columns=[f'item{i}' for i in range(number_products)])
    return df
    
def generate_mock_price_data(cost_dataframe: pd.DataFrame, markup: float=2.4):
    """Generates fake data for cost of products per supplier as a pandas table where rows are suppliers and columns are products
    
    This uses the cost_dataframe generated from "generate_mock_cost_data" and marks the price up by multiplying by markup
    """
    cost = np.array(cost_dataframe)
    P = np.amax(cost, axis=0) 
    P = [p*markup for p in P]
    df = pd.DataFrame([P], columns=cost_dataframe.columns, index=['price'])
    return df

def parse_profit_dataframe(data: pd.DataFrame) -> list[list[str], list[float], list[float]]:
    """Parses the profit dataframe

    Keyword arguments:
    data -- DataFrame of how profit / cost for each product. There must be a "profit" row and "cost" row in the dataframe
    
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
    mock_cost_data = generate_mock_cost_data(20, 10)

    print(mock_cost_data)

    mock_price_data = generate_mock_price_data(mock_cost_data)
    print(mock_price_data)