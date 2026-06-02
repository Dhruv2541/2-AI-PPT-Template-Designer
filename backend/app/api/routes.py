from flask import Blueprint, jsonify

bp = Blueprint("api", __name__)


@bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


# Local import to avoid circular dependency
from app.api.auth import bp as auth_bp
from app.api.templates import bp as templates_bp

bp.register_blueprint(auth_bp)
bp.register_blueprint(templates_bp)
