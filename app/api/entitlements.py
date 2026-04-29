from fastapi import APIRouter, HTTPException
import time
from app.core.firebase import get_db

router = APIRouter(prefix="/entitlements", tags=["Entitlements"])

SECONDS_IN_MONTH = 30 * 24 * 60 * 60


@router.post("/grant")
def grant_entitlement(user_id: str, plan: str, order_id: str):
    db = get_db()
    now = int(time.time())

    if plan not in ("monthly", "lifetime"):
        raise HTTPException(status_code=400, detail="Invalid plan")

    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    # -----------------------------
    # 🚨 DO NOT CREATE NEW USERS
    # -----------------------------
    if not user_doc.exists:
        raise HTTPException(
            status_code=404,
            detail=f"User '{user_id}' not registered"
        )

    # -----------------------------
    # Idempotency
    # -----------------------------
    data = user_doc.to_dict()
    if data.get("last_order_id") == order_id:
        return {"status": "already_granted"}

    # -----------------------------
    # Expiry
    # -----------------------------
    expiry = None

    if plan == "monthly":
        existing_expiry = data.get("entitlement_expiry")
        base = max(existing_expiry or 0, now)
        expiry = base + SECONDS_IN_MONTH

    # -----------------------------
    # Grant entitlement
    # -----------------------------
    user_ref.set(
        {
            "premium": True,
            "plan": plan,
            "entitlement_start": now,
            "entitlement_expiry": expiry,
            "last_order_id": order_id
        },
        merge=True
    )

    return {"status": "granted"}

def grant_entitlement_old(user_id: str, plan: str, order_id: str):
    db = get_db()
    now = int(time.time())

    if plan not in ("monthly", "lifetime"):
        raise HTTPException(status_code=400, detail="Invalid plan")

    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    # -------------------------
    # Idempotency: same order
    # -------------------------
    if user_doc.exists:
        data = user_doc.to_dict()
        if data.get("last_order_id") == order_id:
            return {"status": "already_granted"}

    # -------------------------
    # Compute expiry
    # -------------------------
    expiry = None

    if plan == "monthly":
        # Extend if already active
        existing_expiry = None
        if user_doc.exists:
            existing_expiry = user_doc.to_dict().get("entitlement_expiry")

        base = max(existing_expiry or 0, now)
        expiry = base + SECONDS_IN_MONTH

    # -------------------------
    # Grant / upgrade entitlement
    # -------------------------
    user_ref.set(
        {
            "premium": True,
            "plan": plan,
            "entitlement_start": now,
            "entitlement_expiry": expiry,
            "last_order_id": order_id
        },
        merge=True
    )

    return {"status": "granted"}


@router.get("/{user_id}")
def check_entitlement(user_id: str):
    db = get_db()
    doc = db.collection("users").document(user_id).get()

    if not doc.exists:
        return {
            "is_premium": False,
            "plan": None,
            "expires_at": None
        }

    data = doc.to_dict()
    expiry = data.get("entitlement_expiry")

    # -------------------------
    # Expiry enforcement
    # -------------------------
    if expiry and time.time() > expiry:
        return {
            "is_premium": False,
            "plan": data.get("plan"),
            "expires_at": expiry
        }

    return {
        "is_premium": data.get("premium", False),
        "plan": data.get("plan"),
        "expires_at": expiry
    }
