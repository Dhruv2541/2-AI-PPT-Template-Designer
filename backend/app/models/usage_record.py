import uuid
from datetime import datetime
from sqlalchemy import Uuid, String, Integer, JSON, ForeignKey, DateTime
from app import db


class UsageRecord(db.Model):
    __tablename__ = "usage_records"

    id = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = db.Column(String(100), nullable=False)
    credits_used = db.Column(Integer, nullable=False, default=0)
    details = db.Column(JSON, nullable=True)

    created_at = db.Column(DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("usage_records", lazy=True))
