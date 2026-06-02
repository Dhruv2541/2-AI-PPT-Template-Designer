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
    category = db.Column(
        String(100), nullable=True
    )  # General, Education, Business, etc.

    # Marketplace prep
    is_public = db.Column(Boolean, default=False)
    price = db.Column(Numeric(10, 2), nullable=True, default=0.00)
    status = db.Column(String(50), default="draft")  # draft, published

    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("templates", lazy=True))

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "title": self.title,
            "description": self.description,
            "thumbnail_url": self.thumbnail_url,
            "schema_data": self.schema_data,
            "category": self.category,
            "is_public": self.is_public,
            "price": float(self.price) if self.price else 0.0,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
