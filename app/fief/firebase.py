import firebase_admin
from firebase_admin import db
# from app.main import count
# cred = ${{ secrets.FIREBASE_AUTH_TOKEN }}

cred = {
  "type": "service_account",  #
  "project_id": "shortcuts-38cea",#
  "private_key_id": "c7186234faa4e596f868e4bd5cf2b87aa08387a1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC/Js4popBS85Mf\n8A4MkfDm8c0USoIy8wzOwY5kTOjHxOgNYWz39B+kbWJseANuTSAeKHACkxeHbG/2\nMXqpsV5+8ovYJ5uxdPppTZQbuLnGp41lXUwc/8vRkpzbfjN9u202IrBH04CpF/9v\nbfzYVuTV2D6+kbZIIX3qU/UHxvGGduwZz3wQBKPQ9eTiWH+3v9SCEGNiWWV8A2ov\nixOX2t0tVyTkhB7/c5ARq9N/vPNrVEicPbF6nOy11XAObrlic3SSR/DoUYjP4uul\n1zrmbcZw7cj3W7FmU+hweUKm7J8TPCZLSmhmOs2ZgjNubjq5W6Fsuux4xwVCLI/g\noubAcwTrAgMBAAECggEAA281jg7zK+Jfdtfv0K8Alo2qox4xl6vBQ6e7oLa3CfvS\nNYdWF2Bl/yTN+2fum9k75f7RAGLXLeI3YsOB0jGzInHGLHSNuhMBesnfit33TIfv\nJO6Xsv+vkEzjj5gFYdFvxWS7KRc2PROGzeA6hkKNawAvJGpmzYX4hrDKesDKzyEk\n1pO/6t2F3p6jrMDGZyLSLtlnOSYR9Hy688Q20/Ca3yjBxbp7LjtQZKkAVgW06yTi\nKa8xkq+2jaEmavTdtuFXYC8Ft8tvMYe4TMYhCDGitBuktrrmyNEd0oGsyHKQKc0R\n5RXf0+hjVPuu7+8ioLTwksPZnobes9sZrNA8PTRwRQKBgQD+t68KLm5jyKIS3lt3\nCKt+4Hem9Oy2e9ZaOHbAHoYgwaBFXaEB7ox8vIkrfHZYyjiYl+ovW1sxNedxo64B\nA4taGrHVsflVElWWoBqZIzBMoVSfDPa4UxPiF4M0J8GKQNCWu0ic+QD6NFSo6+At\nuNnxQFTjhtVwVL19lMPUKVD6vwKBgQDAHTBRItKjk0AUrNFozGGN50H5SndsPlCf\nPShqfGOrZ8XjqS7KuusSCKFMXpQfm5t1MVx5j3yZLuZ7nzIP7u2zTP8HJEQz9y87\nCxQudxw8A3vaJ1pRFCQqhPy7vucd3717T0TiaSgp1/eIM56Pe2/oi/eB2gfs0hVG\nRqxLyDqc1QKBgQCBqV1YMHSPJOWj9z7WJDqwdnFSMuGArx9Zg96nQ6KBcC82wEei\npR0srgihc1UHM8GFo+dZPgb40PjE904vQ++e6XHXVyaV8KRS7aM8ixYeHA3ofP/m\nqpu3fsKSPR6fUwkbgbCf/31I4HSsHI5cl/mRfm73934VFX30PFNHX9TSHwKBgB0t\nEaZw1G6VMVkyecchqvsjEOjsP0DIIfRdFGM/qt9gLjSKABo30vV1LBHuFy7Jsg1V\nRscLXI/jCIvjvHWhAqaFXgHWpykBNEISR6la24XdvZR+/39qwKdYdQ2KS41E6oDs\no/iCod/g9a3QsRb3VyKJBzjIRQXZTfPTTd1gdk5VAoGBANwb5etGBOofg9mSo23X\nGv8dnbQNdMkQ+PJFCzdxN1uLhTxxyqKL+IpFlC95j6mQTuEenM+r2qASAzoyjT0w\nd5FVSrphGyag/cEJgztEA8w8elstn6fYsITA7ziCGffvhNRL4wogcmnMUR4bcLp4\ncTNZtD0CRTFFhlh4VM6MYOXp\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-58295@shortcuts-38cea.iam.gserviceaccount.com",
  "client_id": "105399648545530018911",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-58295%40shortcuts-38cea.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

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
    return  get_count_ref.get()


def delete_routine():
 return db.reference('/shortCuts').get()

def get_count_reference():
   db.reference('/shortCuts').delete()

def delete_link(ref):
   db.reference(f'/shortCuts/{ref}').delete()

def push_updated_data(data):
   count_ref.set(data)











   
