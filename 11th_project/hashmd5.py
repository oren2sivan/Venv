import hashlib

def hash(password):
    return hashlib.md5(password.encode()).hexdigest()
