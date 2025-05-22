class UsernameAlreadyExistsException(Exception):
    def __init__(self, username):
        super().__init__(f"User with username '{username}' already exists in the database.")

class NationalNumberAlreadyExistsException(Exception):
    def __init__(self, national_number):
        super().__init__(f"User with national number '{national_number}' already exists in the database.")

class UsernameNotExistsException(Exception):
    def __init__(self, username):
        super().__init__(f"User with username '{username}' does not exist in the database.")


