from flask import Blueprint, jsonify, request

from application.services.auth_service import create_jwt, create_user, verify_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    payload = request.get_json(silent=True) or request.form.to_dict()
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or len(password) < 6:
        return jsonify({"error": "Username and password(min 6 chars) are required"}), 400

    if not create_user(username, password):
        return jsonify({"error": "Username already exists"}), 409

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or request.form.to_dict()
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    user = verify_user(username, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_jwt(user["id"], user["username"])
    return jsonify({"token": token, "user": user})
