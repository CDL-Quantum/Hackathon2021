# Script to seed our mock data

from utils.data import generate_mock_data
from config import standard_mock_data
import os

if __name__ == "__main__":
    for size in standard_mock_data:
        cost_savename = os.path.basename(standard_mock_data[size])
        if size == 'small': 
            generate_mock_data(20, 10, save_name=cost_savename)
        elif size == 'medium':
            generate_mock_data(100, 40, save_name=cost_savename)
        elif size == 'large': 
            generate_mock_data(200, 80, save_name=cost_savename)
        elif size == 'extra_large':
            generate_mock_data(1000, 120, save_name=cost_savename)
        else:
            raise ValueError((f'Unexpected value {size}'))
