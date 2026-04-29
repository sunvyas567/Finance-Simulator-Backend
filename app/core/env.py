# core/env.py
from dotenv import load_dotenv, find_dotenv
import os

def load_env():
    if os.getenv("ENV_LOADED") == "1":
        return

    env_path = find_dotenv()
    load_dotenv(env_path, override=True)

    os.environ["ENV_LOADED"] = "1"
