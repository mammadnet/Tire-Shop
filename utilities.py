from hashlib import sha256
import threading
from platform import system
from datetime import datetime

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

def get_current_datetime():
    now = datetime.now()
    # Format: YYYYMMDD_HHMMSS
    return now.strftime("%Y%m%d_%H%M%S")