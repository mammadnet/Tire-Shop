# Import necessary modules
from hashlib import sha256
import threading
from platform import system

# Function to hash a given string using SHA-256
def hashing(val: str) -> str:
    # Encode the string and compute its SHA-256 hash
    hashed = sha256(val.encode()).hexdigest()
    return hashed

# Class to handle concurrent execution of a function using threading
class Concur:
    def __init__(self, func):
        # Store the function to be executed concurrently
        self.func = func
        # Create a daemon thread for the function
        self.thread = threading.Thread(target=func, daemon=True)
        
    # Start the thread execution
    def start(self):
        self.thread.start()

# Function to check if the operating system is Windows
def is_windows():
    os_name = system()  # Get the name of the operating system
    return os_name == "Windows"

# Function to check if the operating system is Linux
def is_linux():
    os_name = system()  # Get the name of the operating system
    return os_name == "Linux"
