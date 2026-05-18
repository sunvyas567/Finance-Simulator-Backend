from fastapi import APIRouter, HTTPException
from app.core.firebase import get_db

router = APIRouter(prefix="/user-data", tags=["User Data"])
db = get_db()

@router.get("/{username}")
def load_user_data(username: str):
    #print("In load user data", username)
    doc = db.collection("user_data").document(username).get()
    #if doc.exists:
        #print(f"User data found for '{username}': {doc.to_dict()}")
    #    pass
    #else:
    #    print(f"No user data found for '{username}'")
    return doc.to_dict() if doc.exists else {}

#@router.post("/{username}")
#def save_user_data(username: str, data: dict):
#    print("In save user data", username)
#    db.collection("user_data").document(username).set(data)
#    return {"status": "saved"}
@router.post("/save")
def save_user_data(payload: dict):
    username = payload.get("username")
    data = payload.get("data", {})

    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    # 1. Update the 'users' collection (Creates document if it doesn't exist)
    user_ref = db.collection("users").document(username)
    user_ref.set(
        {
            "app_data": data  
        },
        merge=True
    )

    # 2. Update the 'user_data' collection 
    # (CRITICAL: Added merge=True so it doesn't wipe out existing data)
    data_ref = db.collection("user_data").document(username)
    data_ref.set(data, merge=True)

    return {"status": "saved"}

@router.post("/save-old")
def save_user_data(payload: dict):
    #db = get_db()
    username = payload["username"]
    data = payload["data"]
    ref = db.collection("users").document(username)

    #print(f"Attempting to save user data for '{username}' with payload keys: {list(payload.keys())} and data keys: {list(data.keys())}")
    # 🔍 DEBUG (TEMP)
    existing = ref.get().to_dict()
    #print(f"Existing user document for '{username}': {existing}")
    #user_doc = db.collection("users").document(username).get()
    if not existing:
        raise HTTPException(status_code=404, detail="User not registered")

    #print(f"Existing user data for '{username}': {existing}")
    #if "password_hash" not in existing or not existing["password_hash"]:
    #if not existing or "password_hash" not in existing or not existing["password_hash"]:
    #    raise RuntimeError(
    #        f"🚨 Refusing to save: password missing for {username}"
    #    )

    #print("SAVE_USER_DATA DATA:", data)

    ref.set(
        {
            "app_data": data  # ← store app data separately
        },
        merge=True
    )

    #print("SAVE_USER_DATA done for", username)
    username = payload["username"]
    data = payload["data"]

    #print("Saving user_data for:", username)

    db.collection("user_data").document(username).set(data)
    return {"status": "saved"}