# # File holds the class to solve various problems classically (for example: using brute force methods)
import pandas as pd
import numpy as np
from models.data import parse_profit_dataframe

def profit_optimizer(price_data: pd.DataFrame, budget: float):
    """Optimizes the profit problem classically
    
    Keyword arguments:
    price_data -- 1D DataFrame of how much we will charge per item where the columns are the item names and values are the price in floats
    budget -- Float indicating your total budget
    """
    products, price = parse_profit_dataframe(price_data)        
    print('products:\n', products)
    print('price:\n', price)




if __name__ == "__main__":
    import os
    os.chdir('..')    

    # Define some constants
    budget = 100 # 100 dollars buget

    # Fake data (todo: implement this method in Data.py)
    prices = (1.5, 1.4, 1.8, 2.1)
    items = (f'item{i}' for i in range(len(prices)))
    fake_data = pd.DataFrame([prices], columns=items)
    print('Here is our generated data: \n', fake_data)

    profit_optimizer(price_data=fake_data, budget=budget)