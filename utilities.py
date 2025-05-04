from hashlib import sha256
import threading
from platform import system
def hashing(val:str) -> str:
    hashed = sha256(val.encode()).hexdigest()
    return hashed
    

class Concur:
    def __init__(self, func):
        self.func = func
        self.thread = threading.Thread(target=func, daemon=True)
        
    def start(self):
        self.thread.start()
        
        
def is_windows():
    os_name = system()
    return os_name == "Windows"

def is_linux():
    os_name = system()
    return os_name == "Linux"
