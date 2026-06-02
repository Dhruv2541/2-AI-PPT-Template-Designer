from typing import List, Optional
from uuid import UUID
from app.repositories.base import BaseRepository
from app.models.template import Template
from app import db


class TemplateRepository(BaseRepository[Template]):
    def __init__(self):
        super().__init__(Template)

    def get_public_templates(self, category: Optional[str] = None) -> List[Template]:
        query = db.session.query(Template).filter_by(is_public=True)
        if category:
            query = query.filter_by(category=category)
        return query.all()

    def get_user_templates(self, user_id: UUID) -> List[Template]:
        return db.session.query(Template).filter_by(user_id=user_id).all()
