from functools import wraps
import math

from flask import Blueprint, jsonify, request

from application.models.db import get_connection
from application.services.auth_service import decode_jwt, get_bearer_token
from application.services.data_service import (
    get_mandi_comparison,
    get_profit_analysis,
    get_recommendations,
    get_states,
)
from application.services.weather_service import get_weather

api_bp = Blueprint("api", __name__)


def auth_required(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        token = get_bearer_token(request.headers.get("Authorization", ""))
        claims = decode_jwt(token) if token else None
        if not claims:
            return jsonify({"error": "Unauthorized"}), 401
        request.user = claims
        return handler(*args, **kwargs)

    return wrapper


def _save_history(user_id: int, state: str, crop: str, profit: float):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO history (user_id, state, selected_crop, predicted_profit, query_type)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, state, crop, profit, "profit_forecast"),
        )


def _sanitize_json(value):
    if isinstance(value, dict):
        return {k: _sanitize_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_sanitize_json(v) for v in value]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


@api_bp.get("/dashboard")
@auth_required
def dashboard_meta():
    return jsonify(_sanitize_json({"states": get_states()}))


@api_bp.post("/recommend")
@auth_required
def recommend():
    payload = request.get_json(silent=True) or {}
    state = (payload.get("state") or "").strip()
    top_k = int(payload.get("top_k", 5))
    if not state:
        return jsonify({"error": "state is required"}), 400
    data = get_recommendations(state, top_k=top_k)
    if not data:
        return jsonify({"error": "No recommendations found"}), 404
    first = data[0]
    approx_profit = (first["predicted_yield"] * first["modal_price"]) - first["estimated_cost_per_hectare"]
    _save_history(request.user["sub"], state, first["crop"], float(approx_profit))
    return jsonify(_sanitize_json({"state": state, "recommendations": data}))


@api_bp.post("/profit")
@auth_required
def profit():
    payload = request.get_json(silent=True) or {}
    state = (payload.get("state") or "").strip()
    top_k = int(payload.get("top_k", 5))
    if not state:
        return jsonify({"error": "state is required"}), 400

    analysis = get_profit_analysis(state, top_k=top_k)
    if not analysis:
        return jsonify({"error": "No profit data found"}), 404

    best = analysis[0]
    _save_history(
        request.user["sub"],
        state,
        best["crop"],
        float(best["expected_profit"]),
    )
    return jsonify(_sanitize_json({"state": state, "top_crops": analysis, "best_crop": best}))


@api_bp.get("/mandi")
@auth_required
def mandi():
    state = (request.args.get("state") or "").strip()
    crop = (request.args.get("crop") or "").strip()
    if not state:
        return jsonify({"error": "state is required"}), 400
    rows = get_mandi_comparison(state, crop=crop, limit=20)
    if not rows:
        return jsonify({"error": "No mandi data found"}), 404
    return jsonify(_sanitize_json({"state": state, "crop": crop or None, "rows": rows, "best": rows[0]}))


@api_bp.get("/weather")
@auth_required
def weather():
    state = (request.args.get("state") or "").strip()
    if not state:
        return jsonify({"error": "state is required"}), 400
    data = get_weather(state)
    return jsonify(_sanitize_json({"state": state, "weather": data}))


@api_bp.get("/history")
@auth_required
def history():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT state, selected_crop, predicted_profit, query_type, created_at
            FROM history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 50
            """,
            (request.user["sub"],),
        ).fetchall()

    return jsonify(_sanitize_json({"history": [dict(row) for row in rows]}))
