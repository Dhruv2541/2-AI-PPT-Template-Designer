import uuid
from datetime import datetime
from sqlalchemy import (
    Uuid,
    String,
    Boolean,
    Integer,
    ForeignKey,
    DateTime,
    Enum as SQLEnum,
)
import enum
from app import db


class GenerationMode(enum.Enum):
    FAST = "fast"
    DEEP_RESEARCH = "deep_research"
    ACADEMIC = "academic"
    PITCH_DECK = "pitch_deck"
    BUSINESS_REPORT = "business_report"


class Presentation(db.Model):
    __tablename__ = "presentations"

    id = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = db.Column(String(255), nullable=False)
    generation_mode = db.Column(SQLEnum(GenerationMode), nullable=True)

    # Future collaboration support
    version = db.Column(Integer, default=1, nullable=False)
    is_collaborative = db.Column(Boolean, default=False)
    locked_by = db.Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=True)

    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship(
        "User", foreign_keys=[user_id], backref=db.backref("presentations", lazy=True)
    )
    locked_by_user = db.relationship("User", foreign_keys=[locked_by])

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "title": self.title,
            "generation_mode": (
                self.generation_mode.value if self.generation_mode else None
            ),
            "version": self.version,
            "is_collaborative": self.is_collaborative,
            "locked_by": str(self.locked_by) if self.locked_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
