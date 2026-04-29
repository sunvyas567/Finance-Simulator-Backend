from fastapi import APIRouter, HTTPException
from app.api.projection_engine import run_projection_engine

router = APIRouter()

@router.post("/")
def projections_endpoint(payload: dict):
    # Defensive checks (DO NOT BREAK UI)
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Invalid payload")

    user_data = payload.get("user_data")
    user = payload.get("user")

    if user_data is None or user is None:
        raise HTTPException(
            status_code=422,
            detail="Payload must contain 'user_data' and 'user'"
        )

    # Optional debug (safe to keep during dev)
    #print("DEBUG projections payload user:", user.get("username"))
   # print(
   #     "DEBUG projection years:",
   #     user_data.get("GLProjectionYears", {}).get("input")
   # )

    return run_projection_engine(
        user_data=user_data,
        user=user
    )
