from typing import List
from uuid import UUID
from app.repositories.base import BaseRepository
from app.models.asset import Asset
from app import db


class AssetRepository(BaseRepository[Asset]):
    def __init__(self):
        super().__init__(Asset)

    def get_by_user_id(self, user_id: UUID) -> List[Asset]:
        return db.session.query(Asset).filter_by(user_id=user_id).all()
