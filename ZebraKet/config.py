import os

data_dir = os.path.join('.', 'data')
missing_product_price = -1  # put into price matrix when supplier does not have a product
standard_mock_data = dict(
    small = dict(
        price = os.path.join(data_dir, 'small-price-mock.csv'),    
        cost = os.path.join(data_dir, 'small-cost-mock.csv')
    ),
    medium = dict(
        price = os.path.join(data_dir, 'medum-price-mock.csv'),    
        cost = os.path.join(data_dir, 'medium-cost-mock.csv')
    ),
    large = dict(
        price = os.path.join(data_dir, 'large-price-mock.csv'),    
        cost = os.path.join(data_dir, 'large-cost-mock.csv')
    ),
    extra_large = dict(
        price = os.path.join(data_dir, 'extra_large-price-mock.csv'),    
        cost = os.path.join(data_dir, 'extra_large-cost-mock.csv')
    )
)