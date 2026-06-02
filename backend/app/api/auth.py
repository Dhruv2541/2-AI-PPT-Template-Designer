from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db
from datetime import datetime, timedelta
import uuid

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/mock-login", methods=["POST"])
def mock_login():
    """
    MOCK ENDPOINT: Do not use in production.
    Simulates Google OAuth login by finding or creating a test user.
    """
    data = request.get_json() or {}
    email = data.get("email", "teststudent@example.com")
    name = data.get("name", "Test Student")

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            email=email,
            name=name,
            avatar_url="https://ui-avatars.com/api/?name=Test+Student",
        )
        db.session.add(user)
    else:
        user.last_login = datetime.utcnow()

    db.session.commit()

    access_token = create_access_token(
        identity=str(user.id), expires_delta=timedelta(days=1)
    )

    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200


@bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, uuid.UUID(current_user_id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200
