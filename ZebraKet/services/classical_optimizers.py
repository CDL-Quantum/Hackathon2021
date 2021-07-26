# # File holds the class to solve various problems classically (for example: using brute force methods)
import pandas as pd
import numpy as np
from itertools import combinations
from models.data import parse_profit_dataframe

def binary_profit_optimizer(price_data: pd.DataFrame, budget: float) -> tuple[list[int], float, float]:
    """Optimizes the profit problem classically using a binary formulation
    
    Keyword arguments:
    price_data -- 1D DataFrame of how much we will charge per item where the columns are the item names and values are the price in floats
    budget -- Float indicating your total budget

    Returns 
    Tuple of integers indicating the solution
    Maximum cost found
    Maximum weight found
    """
    products, cost, price = parse_profit_dataframe(price_data)        

    print('products:\n', products)
    print('price:\n', price)

    number_of_products = len(products)
    price_cumulative = 0
    cost_cumulative = 0
    result = []

    for product_index in range(1, number_of_products + 1):
        for product_index_combinations in combinations(np.arange(number_of_products), product_index):
            cost_combinations = [cost[i] for i in product_index_combinations]
            price_combinations = [price[i] for i in product_index_combinations]
            running_cost = np.sum(cost_combinations)
            running_price = np.sum(price_combinations)
            if running_cost <= budget and running_price > price_cumulative:
                price_cumulative = running_price
                cost_cumulative = running_cost
                result = product_index_combinations

    return result, cost_cumulative, price_cumulative

if __name__ == "__main__":

    # Define some constants
    budget = 100 # 100 dollars buget

    # Fake data (todo: implement this method in Data.py)
    prices = (3.5, 3.4, 3.8, 6.1)
    costs = (1.5, 1.4, 1.8, 2.1)
    items = (f'item{i}' for i in range(len(prices)))
    row_names = ['price', 'cost']
    fake_data = pd.DataFrame([prices, costs], columns=items, index=row_names)
    print('Here is our generated data: \n', fake_data)

    result, max_cost, max_price = binary_profit_optimizer(price_data=fake_data, budget=budget)
    print('found solution: ', max_cost, max_price)
    print('result\n', result)