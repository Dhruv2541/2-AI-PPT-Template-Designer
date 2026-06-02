from typing import List
from uuid import UUID
from app.repositories.base import BaseRepository
from app.models.presentation import Presentation
from app import db


class PresentationRepository(BaseRepository[Presentation]):
    def __init__(self):
        super().__init__(Presentation)

    def get_by_user_id(self, user_id: UUID) -> List[Presentation]:
        return db.session.query(Presentation).filter_by(user_id=user_id).all()
