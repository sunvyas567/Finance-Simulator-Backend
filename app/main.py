

# main.py (TOP OF FILE)
from app.core.env import load_env
load_env()  # 🔥 must be first

from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
import os

#env_path = find_dotenv()
#print("Found .env at:", env_path)

#loaded = load_dotenv(env_path, override=True)
#print("load_dotenv() returned:", loaded)

#print("FIREBASE_SERVICE_ACCOUNT exists:", "FIREBASE_SERVICE_ACCOUNT" in os.environ)

from app.api import config, user_data, projections, payments, entitlements,users
from webhook import razorpay_webhook
from app.api.advisor.engine import router as advisor_router
from app.api import auth



app = FastAPI(title="Retirement Finance Backend")


#load_dotenv(verbose=True)
app.include_router(config.router)
app.include_router(user_data.router)
#app.include_router(projections.router)
app.include_router(
    projections.router,
    prefix="/projections",
    tags=["projections"]
)
app.include_router(payments.router)
app.include_router(entitlements.router)
app.include_router(razorpay_webhook.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(advisor_router)
