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
    if country in post.find_one({"_id": unique_id})["analytics"].keys():
      post.update_many({"_id": unique_id}, {"$inc": {"count": 1, f"analytics.{country}": 1}})
    else:
      post.update_many({"_id": unique_id}, {"$inc": {"count": 1},"$set": {f"analytics.{country}": 1}})
    print('[INFO] 🥑 Updated Count')


def get_count(unique_id):
    print("[INFO] GOT COUNT FROM SERVER")
    analytics_obj = post.find_one({"_id": unique_id})
    del analytics_obj["_id"]
    print(analytics_obj)
    return analytics_obj

def delete_link(unique_id):
    print(unique_id)
    post.delete_one({"_id": unique_id})


# print(get_count(id))
# update_count(id)
# print(get_count(id))
# delete_job(id)
# print(get_count(id))
