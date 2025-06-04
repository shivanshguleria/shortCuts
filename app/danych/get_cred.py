import json
import os


class Credentials:    
    postgres = os.getenv("postgres_uri")
    mongo = os.getenv("mongo_uri")
