from hashlib import sha256


def hashing(val:str) -> str:
    hashed = sha256(val.encode()).hexdigest()
    return hashed
    
