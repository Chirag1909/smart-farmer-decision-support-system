from flask import Blueprint, render_template, jsonify

pages_bp = Blueprint("pages", __name__)


@pages_bp.get("/health")
def health_check():
    return jsonify({"status": "healthy", "message": "Server is running"}), 200


@pages_bp.get("/")
def home():
    return render_template("login.html")


@pages_bp.get("/login-page")
def login_page():
    return render_template("login.html")


@pages_bp.get("/register-page")
def register_page():
    return render_template("register.html")


@pages_bp.get("/dashboard-page")
def dashboard_page():
    return render_template("dashboard.html")
