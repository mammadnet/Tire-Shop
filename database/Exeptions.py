class UsernameAlreadyExistsException(Exception):
    def __init__(self, username):
        super().__init__(f"User with username '{username}' already exists in the database.")

class NationalNumberAlreadyExistsException(Exception):
    def __init__(self, national_number):
        super().__init__(f"User with national number '{national_number}' already exists in the database.")

class UsernameNotExistsException(Exception):
    def __init__(self, username):
        super().__init__(f"User with username '{username}' does not exist in the database.")

class NoDataFoundError(Exception):

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.message = f"No data found in the table '{self.table_name}'."
        super().__init__(self.message)

class ProductAlreadyExistsException(Exception):
    def __init__(self, product_name):
        super().__init__(f"Product '{product_name}' already exists in the database.")
        
class ProductNotExistsException(Exception):
    def __init__(self, product_name):
        super().__init__(f"Product '{product_name}' does not exist in the database.")

class CustomerNotExistsException(Exception):
    def __init__(self, customer_id):
        super().__init__(f"Customer with ID '{customer_id}' does not exist in the database.")