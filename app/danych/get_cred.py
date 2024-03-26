import json
import os



class Credentials:
    with open("../cred.json") as __cred_file:
        __dict_obj = json.loads(__cred_file.read())
    
    postgres = __dict_obj["postgres_uri"]
    mongo = __dict_obj["mongo_uri"]
