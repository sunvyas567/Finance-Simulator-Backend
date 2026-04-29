# core/firebase.py NEW
import firebase_admin
from firebase_admin import credentials, firestore, auth
import json, os

_db = None


def _initialize():
    """
    Initialize Firebase once.
    Uses FIREBASE_SERVICE_ACCOUNT env var (unchanged).
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
        )
        firebase_admin.initialize_app(cred)


# -------------------------------------------------
# Firestore
# -------------------------------------------------
def get_db():
    global _db

    if _db:
        return _db

    _initialize()
    _db = firestore.client()
    return _db


# -------------------------------------------------
# Firebase Auth (NEW)
# -------------------------------------------------
def get_auth():
    _initialize()
    return auth

# core/firebase.py --OLD
#import firebase_admin
#from firebase_admin import credentials, firestore
#import json, os

#_db = None

#def get_db():
#    global _db

#    if _db:
#        return _db

#    if not firebase_admin._apps:
#        cred = credentials.Certificate(
#            json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
#        )
#        firebase_admin.initialize_app(cred)

#    _db = firestore.client()
#    return _db


