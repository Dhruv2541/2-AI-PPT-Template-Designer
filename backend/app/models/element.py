import uuid
from datetime import datetime
from sqlalchemy import Uuid, Integer, String, JSON, ForeignKey, DateTime
from app import db


class Element(db.Model):
    __tablename__ = "elements"

    id = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slide_id = db.Column(
        Uuid(as_uuid=True), ForeignKey("slides.id", ondelete="CASCADE"), nullable=False
    )
    element_type = db.Column(String(50), nullable=False)  # text, image, shape
    content = db.Column(JSON, nullable=True)
    properties = db.Column(JSON, nullable=False)  # {x, y, w, h, rotation}
    z_index = db.Column(Integer, default=0)

    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    slide = db.relationship(
        "Slide", backref=db.backref("elements", cascade="all, delete-orphan", lazy=True)
    )
