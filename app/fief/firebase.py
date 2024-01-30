import os
import firebase_admin
from firebase_util import create_cred_dict 
from firebase_admin import db
# from app.main import count
# cred = ${{ secrets.FIREBASE_AUTH_TOKEN }}

CRED_OBJ = os.getenv('cred_obj')
CRED_OBJ_KEYS = os.getenv('cred_obj_keys')

cred = create_cred_dict(CRED_OBJ, CRED_OBJ_KEYS)

cred_obj = firebase_admin.credentials.Certificate(cred)
# FIREBASE_URI = os.getenv('FIREBASEURL')
default_app = firebase_admin.initialize_app(cred_obj, {
'databaseURL':  'https://shortcuts-38cea-default-rtdb.asia-southeast1.firebasedatabase.app/'
	})

ref = db.reference('/')

count_ref = ref.child("shortCuts")
# count_ref1 = ref.child("pussy")
def push_new_count(ref):
  # new_short_link_ref = count_ref.push()
  count_ref.child(ref).set({
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
    print("[INFO] GOT COUNT FROM SERVER")
    return {"count": get_count_ref.get()}


def delete_routine():
 return db.reference('/shortCuts').get()

def get_count_reference():
   db.reference('/shortCuts').delete()

def delete_link(ref):
   db.reference(f'/shortCuts/{ref}').delete()

def push_updated_data(data):
   count_ref.set(data)
