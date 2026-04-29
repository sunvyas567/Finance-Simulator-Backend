# webhook/razorpay_webhook.py

from fastapi import APIRouter, Request, HTTPException
import os, json, time
import razorpay
from app.core.firebase import get_db
from app.api.entitlements import grant_entitlement

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

client = razorpay.Client(
    auth=(
        os.environ["RAZORPAY_KEY_ID"],
        os.environ["RAZORPAY_KEY_SECRET"]
    )
)

WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")

if not WEBHOOK_SECRET:
    raise RuntimeError("RAZORPAY_WEBHOOK_SECRET is not set in environment")

#WEBHOOK_SECRET = os.environ["RAZORPAY_WEBHOOK_SECRET"]


@router.post("/razorpay/webhook")
#@router.post("/webhook")
async def razorpay_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("x-razorpay-signature")

    print(f"Rpay signature received: {signature}")
    # 1️⃣ Verify signature
    try:
        client.utility.verify_webhook_signature(
            body.decode(),
            signature,
            WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    payload = json.loads(body)
    event_id = payload.get("id")
    event_type = payload.get("event")

    db = get_db()

    # 2️⃣ Idempotency guard
    processed_ref = db.collection("processed_webhook_events").document(event_id)
    if processed_ref.get().exists:
        return {"status": "duplicate_ignored"}

    processed_ref.set({
        "event_id": event_id,
        "event": event_type,
        "processed_at": int(time.time())
    })

    # 3️⃣ Handle successful payment
    if event_type == "order.paid":
        order = payload["payload"]["order"]["entity"]
        order_id = order["id"]

        payment_ref = db.collection("payments").document(order_id)
        payment_doc = payment_ref.get()

        if not payment_doc.exists:
            raise HTTPException(status_code=400, detail="Unknown order")

        payment = payment_doc.to_dict()

        payment_ref.update({
            "status": "paid",
            "paid_at": int(time.time())
        })
        print(f"Payment marked as paid for order: {order_id}")
        user_id = payment["user_id"]

        # -----------------------------
        # Verify user exists
        # -----------------------------
        user_doc = db.collection("users").document(user_id).get()

        if not user_doc.exists:
            print("🚨 PAYMENT FOR UNKNOWN USER:", user_id)
            raise HTTPException(
                status_code=400,
                detail=f"Payment received for unknown user '{user_id}'"
            )
        print("RAZORPAY PAYMENT USER_ID:", payment["user_id"])

        grant_entitlement(
            user_id=payment["user_id"],
            plan=payment["plan"],
            order_id=order_id
        )

    return {"status": "ok"}
