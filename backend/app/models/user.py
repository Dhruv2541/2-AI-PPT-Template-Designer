import uuid
from datetime import datetime
from sqlalchemy import Uuid
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    google_id = db.Column(db.String(128), unique=True, nullable=True) # Nullable for mock auth
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat()
        }
