# Raised when an attempt is made to create a user with a username that already exists.
class UsernameAlreadyExistsException(Exception):
    def __init__(self, username):
        # Initializes the parent Exception class with a formatted error message.
        super().__init__(f"User with username '{username}' already exists in the database.")

# Raised when an attempt is made to create a user with a national ID that already exists.
class NationalNumberAlreadyExistsException(Exception):
    def __init__(self, national_number):
        super().__init__(f"User with national number '{national_number}' already exists in the database.")

# Raised when a user is queried by a username that does not exist in the database.
class UsernameNotExistsException(Exception):
    def __init__(self, username):
        super().__init__(f"User with username '{username}' does not exist in the database.")

# A generic exception for cases where a database query on a table yields no results.
class NoDataFoundError(Exception):
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.message = f"No data found in the table '{self.table_name}'."
        super().__init__(self.message)

# Raised when an attempt is made to create a product that is already in the database.
class ProductAlreadyExistsException(Exception):
    def __init__(self, product_name):
        super().__init__(f"Product '{product_name}' already exists in the database.")
        
# Raised when a product is queried that does not exist in the database.
class ProductNotExistsException(Exception):
    def __init__(self, product_name):
        super().__init__(f"Product '{product_name}' does not exist in the database.")

# Raised when a customer is queried by an ID that does not exist in the database.
class CustomerNotExistsException(Exception):
    def __init__(self, customer_id):
        super().__init__(f"Customer with ID '{customer_id}' does not exist in the database.")