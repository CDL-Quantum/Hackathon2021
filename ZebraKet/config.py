import os

data_dir = os.path.join('data')
missing_product_price = -1  # put into price matrix when supplier does not have a product
standard_mock_data = dict(
    small = dict(
        price = os.path.join(data_dir, 'price-n_products_20-n_suppliers_10-20210726-210212.csv'),    
        cost = os.path.join(data_dir, 'cost-n_products_20-n_suppliers_10-20210726-210212.csv')
    ),
    medium = dict(
        price = os.path.join(data_dir, 'price-n_products_100-n_suppliers_40-20210726-210212.csv'),    
        cost = os.path.join(data_dir, 'cost-n_products_100-n_suppliers_40-20210726-210212.csv')
    ),
    large = dict(
        price = os.path.join(data_dir, 'price-n_products_200-n_suppliers_80-20210726-210212.csv'),    
        cost = os.path.join(data_dir, 'cost-n_products_200-n_suppliers_80-20210726-210212.csv')
    ),
    extra_large = dict(
        price = os.path.join(data_dir, 'price-n_products_1000-n_suppliers_120-20210726-210212.csv'),    
        cost = os.path.join(data_dir, 'cost-n_products_1000-n_suppliers_120-20210726-210212.csv')
    )
)