import random
import string
import secrets
def genrate_random_string():
    return "".join(random.sample(string.ascii_letters, k =5))

def generate_token():
    return secrets.token_urlsafe(10)

def generate_unique_id():
    return secrets.token_hex(5)
