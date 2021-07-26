# Class to manage data (for example, loading data from csv, generating mock data etc)
import pandas as pd
import numpy as np

def generate_mock_cost_data(number_products=10, number_suppliers=10):
    """Generates fake data for cost of products per supplier as a pandas table where rows are suppliers and columns are products
    """
    pass
    
def generate_mock_profit_data(number_products=10, number_suppliers=10):
    """Generates fake data for cost of products per supplier as a pandas table where rows are suppliers and columns are products
    """
    pass

def parse_profit_dataframe(data: pd.DataFrame) -> list[list[str], list[float], list[float]]:
    """Parses the profit dataframe

    Keyword arguments:
    data -- DataFrame of how profit / cost for each product. There must be a "profit" row and "cost" row in the dataframe
    
    Returns:
    Tuple of product names (str)
    Tuple of product cost (float)
    Tuple of product prices (float)

    Example input: 

            | apples | bananas 
    price   | 6.5    | 7.1
    cost    | 2.5    | 2.4
    """
    return list(data), list(data.loc['cost']), list(data.loc['price'])
