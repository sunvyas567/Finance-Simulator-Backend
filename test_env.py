from dotenv import load_dotenv, find_dotenv
import os

env_path = find_dotenv()
print("Found .env at:", env_path)

loaded = load_dotenv(env_path)
print("load_dotenv() returned:", loaded)

print("FIREBASE_SERVICE_ACCOUNT exists:", "FIREBASE_SERVICE_ACCOUNT" in os.environ)
