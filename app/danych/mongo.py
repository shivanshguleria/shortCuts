from pymongo import MongoClient
from app.danych.get_cred import Credentials
client = MongoClient(Credentials.mongo)


db = client.count_db

collection = db.collection

post = db.posts
def push_new_count(unique_id):
    # post = posts.find_one({"_id": "skjdksj"})["tags"]
    post.insert_one({
        "_id": unique_id,
        "count": 0,
        "analytics": {}
        })
    print("[INFO] 🔥 Pushed Data")

# push_new_count(id)

def update_count(unique_id, country):
    # country_inc = post.find_one({"_id": unique_id})["analytics"]
    post.update_one({"_id": unique_id}, {"$inc": {"count": 1, "analytics": {country: 1}}})
    print('[INFO] 🥑 Updated Count')


def get_count(unique_id):
    print("[INFO] GOT COUNT FROM SERVER")
    return post.find_one({"_id": unique_id})["count"]

def delete_link(unique_id):
    post.delete_one({"_id": unique_id})


# print(get_count(id))
# update_count(id)
# print(get_count(id))
# delete_job(id)
# print(get_count(id))
