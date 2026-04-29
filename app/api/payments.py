# app/payments/payments.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, time, razorpay
from app.core.firebase import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])

# -------------------------
# Plans (paise)
# -------------------------
PLANS = {
    "monthly": 19900,
    "lifetime": 117000
}

def get_client():
    return razorpay.Client(
        auth=(os.environ["RAZORPAY_KEY_ID"], os.environ["RAZORPAY_KEY_SECRET"])
    )

# -------------------------
# API models
# -------------------------
class CreateOrderRequest(BaseModel):
    user_id: str
    plan: str

# -------------------------
# Routes
# -------------------------
@router.post("/create-order")
def create_order(payload: CreateOrderRequest):
    if payload.plan not in PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan")

    db = get_db()
    client = get_client()

    print("In Creating RPAY oerder for plan:", payload.plan)
    # -------------------------
    # Idempotency: reuse active order
    # -------------------------
    existing = (
        db.collection("payments")
        .where("user_id", "==", payload.user_id)
        .where("plan", "==", payload.plan)
        .where("status", "in", ["created", "authorized"])
        .limit(1)
        .stream()
    )

    #for doc in existing:
    #    data = doc.to_dict()
    ##    print("Reusing existing order:", data["order_id"])
    #    return {
    #        "order_id": data["order_id"],
    #        "amount": PLANS[payload.plan],
    #        "currency": "INR",
    #        "razorpay_key": os.environ["RAZORPAY_KEY_ID"]
    #    }

    # -------------------------
    # Create new Razorpay order
    # -------------------------
    print("Creating RPAY oerder for plan:", payload.plan)
    order = client.order.create({
        "amount": PLANS[payload.plan],
        "currency": "INR",
        "payment_capture": 1,
        "notes": {
            "user_id": payload.user_id,
            "plan": payload.plan,
            "billing_type": payload.plan  # monthly | lifetime
        }
    })

    # -------------------------
    # Persist payment intent
    # -------------------------
    db.collection("payments").document(order["id"]).set({
        "order_id": order["id"],
        "user_id": payload.user_id,
        "plan": payload.plan,
        "billing_type": payload.plan,
        "status": "created",
        "created_at": int(time.time())
    })

    return {
        "order_id": order["id"],
        "amount": PLANS[payload.plan],
        "currency": order["currency"],
        "razorpay_key": os.environ["RAZORPAY_KEY_ID"]
    }
