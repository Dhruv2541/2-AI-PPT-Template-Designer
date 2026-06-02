import uuid
from datetime import datetime
from sqlalchemy import Uuid, Integer, JSON, ForeignKey, DateTime, Text
from app import db


class Slide(db.Model):
    __tablename__ = "slides"

    id = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    presentation_id = db.Column(
        Uuid(as_uuid=True),
        ForeignKey("presentations.id", ondelete="CASCADE"),
        nullable=False,
    )
    order_index = db.Column(Integer, nullable=False, default=0)
    background = db.Column(JSON, nullable=True)
    notes = db.Column(Text, nullable=True)

    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    presentation = db.relationship(
        "Presentation",
        backref=db.backref("slides", cascade="all, delete-orphan", lazy=True),
    )
