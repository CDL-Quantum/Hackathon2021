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

def parse_profit_dataframe(data: pd.DataFrame) -> tuple[tuple[str], tuple[float]]:
    """Parses the profit dataframe

    Keyword arguments:
    data -- DataFrame of how much we will sell each item
    
    Returns:
    Tuple of product names (str)
    Tuple of product prices (float)
    """
    return tuple(data), tuple(data.iloc[0])
