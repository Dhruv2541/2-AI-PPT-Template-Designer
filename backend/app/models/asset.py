import uuid
from datetime import datetime
from sqlalchemy import Uuid, String, Integer, ForeignKey, DateTime
from app import db


class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    asset_type = db.Column(String(50), nullable=False)  # image, document
    mime_type = db.Column(String(100), nullable=False)
    storage_path = db.Column(String(500), nullable=False)
    original_filename = db.Column(String(255), nullable=False)
    size_bytes = db.Column(Integer, nullable=False, default=0)

    created_at = db.Column(DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("assets", lazy=True))
