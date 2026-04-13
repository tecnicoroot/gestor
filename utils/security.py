import hashlib

import bcrypt

def hash_password(password):
    if isinstance(password, str):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return password  # já está em bytes

def verify_password(password, hashed):
    return hash_password(password) == hashed