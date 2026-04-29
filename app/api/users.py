from fastapi import APIRouter
from app.core.firebase import get_db

router = APIRouter(tags=["users"])


@router.get("/users/auth/")
def get_users_for_auth():
    """
    Returns users in streamlit-authenticator compatible format
    """
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
    #print("Credentials - 1", credentials)
    return {
        "credentials": credentials,
        "cookie": {
            "name": "finance_sim_cookie",
            "key": "finance_sim_secret_key",
            "expiry_days": 0
        },
        "preauthorized": {
            "emails": []
        }
    }
