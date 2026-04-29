from env import load_env
load_env()  # 🔥 must be first
from streamlit_authenticator.utilities.hasher import Hasher
from firebase import get_db

db = get_db()

users_ref = db.collection("users").stream()
credentials = {"usernames": {}}
for user in users_ref:
        data = user.to_dict()
        username = user.id

        credentials["usernames"][username] = {
            "email": data.get("email"),
            "name": data.get("name"),
            "password": data.get("password_hash"),
        }
print("Credentials - 1", credentials)

username = "amvyas"  # 👈 change this
new_password = "Tempp@1234"  # 👈 give user once, force change later

hashed = Hasher.hash(new_password)

db.collection("users").document(username).update({
    "email": "amol.vyas0630@gmail.com",
    "name": "Amol V",
    "password_hash": hashed,
})

print("✅ Password reset for", username)
for user in users_ref:
        data = user.to_dict()
        username = user.id

        credentials["usernames"][username] = {
            "email": data.get("email"),
            "name": data.get("name"),
            "password": data.get("password_hash"),
        }
print("Credentials - 2", credentials)

