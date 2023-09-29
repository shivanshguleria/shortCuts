import random
import string

def genrate_random_string():
    return "".join(random.sample(string.ascii_letters, k =5))


