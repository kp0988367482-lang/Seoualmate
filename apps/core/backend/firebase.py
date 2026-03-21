import os
import json
from typing import Optional, Any

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    _FIREBASE_AVAILABLE = True
except Exception:
    firebase_admin = None  # type: ignore[assignment]
    credentials = None  # type: ignore[assignment]
    firestore = None  # type: ignore[assignment]
    _FIREBASE_AVAILABLE = False


def init_firebase() -> Optional[Any]:
    """Initialize Firebase Admin SDK.

    Uses either FIREBASE_SA (path to service account JSON file) or
    FIREBASE_SA_JSON (raw JSON string). Returns a Firestore client or None.
    """
    if not _FIREBASE_AVAILABLE or firebase_admin is None:
        return None

    sa_path = os.getenv("FIREBASE_SA")
    sa_json = os.getenv("FIREBASE_SA_JSON")

    try:
        if sa_path and os.path.exists(sa_path):
            cred = credentials.Certificate(sa_path)  # type: ignore[union-attr]
            firebase_admin.initialize_app(cred)  # type: ignore[union-attr]
            return firestore.client()  # type: ignore[union-attr]
        elif sa_json:
            info = json.loads(sa_json)
            cred = credentials.Certificate(info)  # type: ignore[union-attr]
            firebase_admin.initialize_app(cred)  # type: ignore[union-attr]
            return firestore.client()  # type: ignore[union-attr]
    except Exception:
        return None

    return None


# Initialize once
_firestore_client: Optional[Any] = None


def get_firestore() -> Optional[Any]:
    global _firestore_client
    if _firestore_client is None:
        _firestore_client = init_firebase()
    return _firestore_client
