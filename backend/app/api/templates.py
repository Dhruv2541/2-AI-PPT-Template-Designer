from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.template_repository import TemplateRepository
from app.repositories.presentation_repository import PresentationRepository
from app.models.presentation import Presentation
from app.models.template import Template
import uuid

bp = Blueprint("templates", __name__, url_prefix="/templates")


@bp.route("", methods=["GET"])
def list_public_templates():
    category = request.args.get("category")
    repo = TemplateRepository()
    templates = repo.get_public_templates(category=category)
    return jsonify([t.to_dict() for t in templates]), 200


@bp.route("/me", methods=["GET"])
@jwt_required()
def list_user_templates():
    user_id = uuid.UUID(get_jwt_identity())
    repo = TemplateRepository()
    templates = repo.get_user_templates(user_id=user_id)
    return jsonify([t.to_dict() for t in templates]), 200


@bp.route("", methods=["POST"])
@jwt_required()
def create_template():
    user_id = uuid.UUID(get_jwt_identity())
    data = request.get_json()

    if not data or not data.get("title") or not data.get("schema_data"):
        return jsonify({"error": "Missing required fields"}), 400

    repo = TemplateRepository()
    template = Template(
        user_id=user_id,
        title=data["title"],
        description=data.get("description"),
        thumbnail_url=data.get("thumbnail_url"),
        category=data.get("category", "General"),
        schema_data=data["schema_data"],
        is_public=data.get("is_public", False),
    )
    created = repo.create(template)
    return jsonify(created.to_dict()), 201


@bp.route("/<template_id>/duplicate", methods=["POST"])
@jwt_required()
def duplicate_template(template_id):
    user_id = uuid.UUID(get_jwt_identity())

    template_repo = TemplateRepository()
    try:
        template = template_repo.get_by_id(uuid.UUID(template_id))
    except ValueError:
        return jsonify({"error": "Invalid template ID format"}), 400

    if not template:
        return jsonify({"error": "Template not found"}), 404

    # Check access: must be public OR owned by the user
    if not template.is_public and template.user_id != user_id:
        return jsonify({"error": "Unauthorized to duplicate this template"}), 403

    # Duplicate into a new Presentation
    presentation_repo = PresentationRepository()
    presentation = Presentation(
        user_id=user_id,
        title=f"Copy of {template.title}",
        # Note: In a real implementation, you would also parse template.schema_data
        # and create Slide, Element, and Animation records.
        # For scaffolding, we just create the root presentation entity.
    )
    created_presentation = presentation_repo.create(presentation)

    return jsonify(created_presentation.to_dict()), 201
