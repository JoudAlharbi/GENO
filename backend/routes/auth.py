from flask import Blueprint, request, jsonify
from firebase_admin import auth

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/verify")
def verify():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Missing ID token"}), 401
    try:
        decoded = auth.verify_id_token(token)
        return jsonify({"uid": decoded["uid"], "email": decoded.get("email")})
    except Exception:
        return jsonify({"error": "Invalid token"}), 401