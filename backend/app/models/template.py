import uuid
from datetime import datetime
from sqlalchemy import Uuid, String, Boolean, Numeric, JSON, ForeignKey, DateTime, Text
from app import db


class Template(db.Model):
    __tablename__ = "templates"

    id = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=True)
    title = db.Column(String(255), nullable=False)
    description = db.Column(Text, nullable=True)
    thumbnail_url = db.Column(String(255), nullable=True)
    schema_data = db.Column(JSON, nullable=False)

    # Marketplace prep
    is_public = db.Column(Boolean, default=False)
    price = db.Column(Numeric(10, 2), nullable=True, default=0.00)
    status = db.Column(String(50), default="draft")  # draft, published

    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("templates", lazy=True))
