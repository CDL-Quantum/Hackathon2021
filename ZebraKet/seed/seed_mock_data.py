# Script to seed our mock data

from utils.data import generate_mock_data
from config import standard_mock_data
import os

if __name__ == "__main__":
    for size in standard_mock_data:
        price_savename = os.path.basename(standard_mock_data[size]['price'])
        cost_savename = os.path.basename(standard_mock_data[size]['cost'])
        if size == 'small': 
            generate_mock_data(20, 10, price_save_name=price_savename, cost_save_name=cost_savename)
        elif size == 'medium':
            generate_mock_data(100, 40, price_save_name=price_savename, cost_save_name=cost_savename)
        elif size == 'large': 
            generate_mock_data(200, 80, price_save_name=price_savename, cost_save_name=cost_savename)
        elif size == 'extra_large':
            generate_mock_data(1000, 120, price_save_name=price_savename, cost_save_name=cost_savename)
        else:
            raise ValueError((f'Unexpected value {size}'))
