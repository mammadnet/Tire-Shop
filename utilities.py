from hashlib import sha256
import threading

def hashing(val:str) -> str:
    hashed = sha256(val.encode()).hexdigest()
    return hashed
    

class Concur:
    def __init__(self, func):
        self.func = func
        self.thread = threading.Thread(target=func)
        
    def start(self):
        self.thread.start()