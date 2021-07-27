# # File holds the class to solve various problems classically (for example: using brute force methods)
import pandas as pd
import numpy as np
from itertools import combinations
from utils.data import parse_profit_dataframe

def binary_profit_optimizer(profit: list[float], cost: list[float], budget: float) -> tuple[list[int], float, float]:
    """Optimizes the profit problem classically using a binary formulation (AKA items can only be used once)
    
    Keyword arguments:
    profit - list of floats
    cost - list of floats
    budget -- Float indicating your total budget

    Returns 
    Tuple of integers indicating the solution
    Maximum cost found
    Maximum profit found
    """

    number_of_products = len(profit)
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

def discrete_profit_optimizer(profit: list[float], cost: list[float], budget:float) -> tuple[list[int], float, float]:
    """Optimizes the profit problem classically using a discrete formulation (AKA: items can be used more than once)
    
    Keyword arguments:
    profit - list of floats
    cost - list of floats
    budget -- Float indicating your total budget

    Returns 
    Tuple of integers indicating the solution
    Maximum cost found
    Maximum weight found

    TODO: We need to extract the solution and cost of this method
    TODO: We need to add a bound to number of variable chosen
    """

    def unboundedKnapsack(W, n, val, wt):
        # Solution found here: https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed/
        # dp[i] is going to store maximum
        # value with knapsack capacity i.
        dp = [0 for _ in range(W + 1)]  # profit
        # Fill dp[] using above recursive formula
        for i in range(W + 1):
            for j in range(n):
                if (wt[j] <= i):
                    if val[j] + dp[i - wt[j]] > dp[i]:
                        dp[i] = max(dp[i], dp[i - wt[j]] + val[j])

        return dp[W]

    # Need to do some hacky-ness to convert these to integers
    multiplier = 100
    cost_int = [int(c*multiplier) for c in cost]
    profit_int = [int(p*multiplier) for p in profit]
    budget_int = int(budget*multiplier)

    profit_solution_int = unboundedKnapsack(budget_int, len(profit), profit_int, cost_int)

    return profit_solution_int / multiplier

def binary_supplier_optimizer(inventory: list[int or str], supplier_inventory:list[set[int or str]]):
    # Taken from https://www.codegrepper.com/code-examples/python/set+cover+problem+in+python
    # Find a family of subsets that covers the universal set
    inventory_set = set(inventory)
    elements = set(e for s in supplier_inventory for e in s)
    # Check the subsets cover the universe
    if elements != inventory_set:
        return None
    covered = set()
    cover = []
    # Greedily add the subsets with the most uncovered points
    while covered != elements:
        subset = max(supplier_inventory, key=lambda s: len(s - covered))
        cover.append(subset)
        covered |= subset
    return cover

if __name__ == "__main__":

    from utils.data import read_profit_optimization_data, read_inventory_optimization_data
    from config import standard_mock_data

    # Define some constants
    budget = 1000 # 100 dollars buget

    # Example usage of the classical profit optimizers
    profit, cost = read_profit_optimization_data(standard_mock_data['small'])
    
    binary_solution, binary_cost, binary_profit = binary_profit_optimizer(profit=profit, cost=cost, budget=budget)
    print('\n\nFound binary (crude) profit optimization solution', binary_solution, binary_cost, binary_profit)

    # TODO: fix the binary_profit_optimizer to yield solutions + costs
    discrete_profit = discrete_profit_optimizer(profit=profit, cost=cost, budget=budget)
    print('\n\nFound discrete (crude) profit optimization solution', discrete_profit)

    # Example usage of the classical supplier optimizer
    inventory, supplier_inventory = read_inventory_optimization_data(standard_mock_data['small'])
    cover = binary_supplier_optimizer(inventory, supplier_inventory)
    print('\n\nFound cover set solution: ', cover)