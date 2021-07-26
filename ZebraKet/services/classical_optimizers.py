# # File holds the class to solve various problems classically (for example: using brute force methods)
import pandas as pd
import numpy as np
from itertools import combinations
from models.data import parse_profit_dataframe

def binary_profit_optimizer(price_data: pd.DataFrame, budget: float) -> tuple[list[int], float, float]:
    """Optimizes the profit problem classically using a binary formulation (AKA items can only be used once)
    
    Keyword arguments:
    price_data -- 1D DataFrame of how much we will charge per item where the columns are the item names and values are the price in floats
    budget -- Float indicating your total budget

    Returns 
    Tuple of integers indicating the solution
    Maximum cost found
    Maximum profit found
    """
    products, cost, profit = parse_profit_dataframe(price_data)

    print('products:\n', products)
    print('price:\n', profit)

    number_of_products = len(products)
    profit_cumulative = 0
    cost_cumulative = 0
    result = []

    for product_index in range(1, number_of_products + 1):
        for product_index_combinations in combinations(np.arange(number_of_products), product_index):
            cost_combinations = [cost[i] for i in product_index_combinations]
            profit_combinations = [profit[i] for i in product_index_combinations]
            running_cost = np.sum(cost_combinations)
            running_profit = np.sum(profit_combinations)
            if running_cost <= budget and running_profit > profit_cumulative:
                profit_cumulative = running_profit
                cost_cumulative = running_cost
                result = product_index_combinations

    return result, cost_cumulative, profit_cumulative

def discrete_profit_optimizer(price_data: pd.DataFrame, budget:float) -> tuple[list[int], float, float]:
    """Optimizes the profit problem classically using a discrete formulation (AKA: items can be used more than once)
    
    Keyword arguments:
    price_data -- 1D DataFrame of how much we will charge per item where the columns are the item names and values are the price in floats
    budget -- Float indicating your total budget

    Returns 
    Tuple of integers indicating the solution
    Maximum cost found
    Maximum weight found
    """

    def unboundedKnapsack(W, n, val, wt):
        # Solution found here: https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed/
        # dp[i] is going to store maximum
        # value with knapsack capacity i.
        dp = [0 for _ in range(W + 1)]  # profit
        cost = [0 for _ in range(W + 1)]
        solution_set = [[0 for _ in range(n)] for _ in range(W + 1)]
        # Fill dp[] using above recursive formula
        for i in range(W + 1):
            for j in range(n):
                if (wt[j] <= i):
                    if val[j] + dp[i - wt[j]] > dp[i]:
                        dp[i] = max(dp[i], dp[i - wt[j]] + val[j])
                        solution_set[i][j] += 1
                        cost[i] += wt[j]
                    else:
                        solution_set[i][j] = solution_set[i][j - 1]
                        cost[i] = cost[i-1]

        return solution_set[W], cost[W], dp[W]

    products, cost, profit = parse_profit_dataframe(price_data)

    # Need to do some hacky-ness to convert these to integers
    multiplier = 100
    cost_int = [int(c*multiplier) for c in cost]
    profit_int = [int(p*multiplier) for p in profit]
    budget_int = int(budget*multiplier)

    solution, cost_solution_int, profit_solution_int = unboundedKnapsack(budget_int, len(products), profit_int, cost_int)

    ####### TODO: fix this: profit_solution_int is the only accurate number. Need a better way to track the solution + cost

    return solution, cost_solution_int / multiplier, profit_solution_int / multiplier


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

    discrete_solution, discrete_cost, discrete_profit = binary_profit_optimizer(price_data=fake_data, budget=budget)
    print('found solution for BINARY knapsack: ', discrete_cost, discrete_profit)
    print('result\n', discrete_solution, '\n\n')

    binary_solution, binary_cost, binary_profit = discrete_profit_optimizer(price_data=fake_data, budget=budget)
    print('found solution for DISCRETE knapsack: ', binary_cost, binary_profit)
    print('result\n', binary_solution)


