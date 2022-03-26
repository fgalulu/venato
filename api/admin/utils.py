import secrets

def generate_random_password():
    pwd = secrets.token_hex(8)
    return pwd
