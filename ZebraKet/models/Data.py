# Class to manage data (for example, loading data from csv, generating mock data etc)
class Data:
    def __init__(self, save_directory="data"):
        self.save_directory = save_directory

    @staticmethod
    def generate_mock_cost_data(number_products=10, number_suppliers=10):
        """Generates fake data for cost of products per supplier as a pandas table where rows are suppliers and columns are products
        """
        

    @staticmethod
    def generate_mock_profit_data(number_products=10, number_suppliers=10):
        """Generates fake data for cost of products per supplier as a pandas table where rows are suppliers and columns are products
        """
        pass
