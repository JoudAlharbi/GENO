import os
from functools import wraps
from flask import request, jsonify
from firebase_admin import auth

DEV_MODE = os.getenv("PROJECT_ENV", "dev") == "dev"

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if DEV_MODE:
            request.user = {"uid": "dev-user-123", "email": "dev@example.com"}
            return fn(*args, **kwargs)
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Missing ID token"}), 401
        try:
            request.user = auth.verify_id_token(token)
        except Exception:
            return jsonify({"error": "Invalid token"}), 401
        return fn(*args, **kwargs)
    return wrapper