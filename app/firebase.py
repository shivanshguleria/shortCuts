import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os,json


cred = ${{ secrets.FIREBASE_AUTH_TOKEN }}
cred_obj = firebase_admin.credentials.Certificate(cred)
FIREBASE_URI = os.getenv('FIREBASEURL')
default_app = firebase_admin.initialize_app(cred_obj, {
'databaseURL':  FIREBASE_URI
	})

ref = db.reference('/')

count_ref = ref.child("shortCuts")

def push_new_count(shrt_link):
  # new_short_link_ref = count_ref.push()
  count_ref.child(shrt_link).set({
      'count': 0
 })
#   count_ref.set({
#       shrt_link : {
#       'count': 0
#         }   
#   })

  print("[INFO] 🔥 Pushed Data")


def increment_count(current_value):
    # print(current_value)
    return current_value + 1 if current_value else 1

def update_count(ref):
    update_count_ref = db.reference("shortCuts/" + ref + "/count")
    try:
        new_count_ref = update_count_ref.transaction(increment_count)
        print('[INFO] 🥑 Updated Count')
    except db.TransactionAbortedError:
        print('[ERR] Transaction failed to commit')
    return update_count_ref.get()
  # print(new_short_link_ref.key)

def get_count(ref):
    get_count_ref = db.reference(f'shortCuts/{ref}/count')
    return get_count_ref.get()


  