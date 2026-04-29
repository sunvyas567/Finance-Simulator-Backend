from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
import streamlit_authenticator as stauth

from app.core.firebase import get_db, get_auth

router = APIRouter(prefix="/auth", tags=["auth"])

db = get_db()
firebase_auth = get_auth()


# ================================
# Request model
# ================================
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


# ================================
# Register user
# ================================
@router.post("/register")
def register_user(req: RegisterRequest):

    username = req.email.split("@")[0]

    # prevent duplicate
    if db.collection("users").document(username).get().exists:
        raise HTTPException(400, "User already exists")

    # -----------------------------
    # Create Firebase Auth user
    # -----------------------------
    user = firebase_auth.create_user(
        email=req.email,
        password=req.password,
        display_name=req.name
    )

    # -----------------------------
    # Hash password for Streamlit
    # -----------------------------
    #hashed = stauth.Hasher([req.password]).generate()[0]
    hashed = stauth.Hasher.hash(req.password)


    # -----------------------------
    # Firestore profile
    # -----------------------------
    db.collection("users").document(username).set({
        "uid": user.uid,
        "email": req.email,
        "name": req.name,
        "password_hash": hashed,
        "created_at": datetime.utcnow(),
        "app_data": {}
    })

    return {
        "status": "created",
        "username": username
    }
