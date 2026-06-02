import uuid
from datetime import datetime
from sqlalchemy import Uuid, Integer, String, Float, JSON, ForeignKey, DateTime
from app import db


class Animation(db.Model):
    __tablename__ = "animations"

    id = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    element_id = db.Column(
        Uuid(as_uuid=True),
        ForeignKey("elements.id", ondelete="CASCADE"),
        nullable=False,
    )
    animation_type = db.Column(String(50), nullable=False)
    duration = db.Column(Float, nullable=False, default=1.0)
    delay = db.Column(Float, nullable=False, default=0.0)
    order_index = db.Column(Integer, nullable=False, default=0)
    properties = db.Column(JSON, nullable=True)

    created_at = db.Column(DateTime, default=datetime.utcnow)

    element = db.relationship(
        "Element",
        backref=db.backref("animations", cascade="all, delete-orphan", lazy=True),
    )
