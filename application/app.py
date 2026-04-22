import os
from flask import Flask
from dotenv import load_dotenv

from application.models.db import init_db
from application.routes.auth import auth_bp
from application.routes.api import api_bp
from application.routes.pages import pages_bp


def create_app() -> Flask:
    load_dotenv()
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY", "change-this-in-production")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", app.config["SECRET_KEY"])

    init_db()
    app.register_blueprint(pages_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
