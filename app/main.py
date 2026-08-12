

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
# 1. Import the CORS middleware component
from fastapi.middleware.cors import CORSMiddleware

# 2. Define the list of allowed frontend origins.
# Include both localhost and your mobile testing configurations!
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # 💡 Pro Tip: If you are testing on mobile web via your Wi-Fi IP network, 
    # add your MacBook Pro's local network IP address here too:
    # "http://192.168.1.35:5173", 
]

app = FastAPI(title="Retirement Finance Backend")

# 3. Inject the middleware parameters into your engine configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Alternately use origins for localhost testing access
    allow_credentials=True,
    allow_methods=["*"],              # Allows GET, POST, OPTIONS, PUT, DELETE
    allow_headers=["*"],              # Allows Authorization and Content-Type headers
)
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
