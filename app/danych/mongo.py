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

def update_count(unique_id, country = None):
    # countries = post.find_one({"_id": unique_id})

   # process data if not  Nonetype, usefull when analytics  database destroyed 
    # if countries is not None and country in countries["analytics"].keys():
    #   post.update_many({"_id": unique_id}, {"$inc": {"count": 1, f"analytics.{country}": 1}})
    # else:
    #   post.update_many({"_id": unique_id}, {"$inc": {"count": 1},"$set": {f"analytics.{country}": 1}})
    post.find_one_and_update({"_id": unique_id}, {"$inc": {"count": 1, f"analytics.{country}": 1}}, upsert=True)
    print('[INFO] 🥑 Updated Count')


def get_count(unique_id):
    print("[INFO] GOT COUNT FROM SERVER")
    analytics_obj = post.find_one({"_id": unique_id}, {"_id": 0}) 
    print(analytics_obj)
    return analytics_obj

def delete_link(unique_id):
    print(unique_id)
    post.delete_one({"_id": unique_id})

def delete_link_upsert(id):
    print(id)
    print(post.update_one({"_id": id}, {'$set':{"is_alive": False}}, upsert=True))
def find_unique_id(uid):
   return post.find_one({"_id": uid})


# print(get_count(id))
# update_count(id)
# print(get_count(id))
# delete_job(id)
# print(get_count(id))
