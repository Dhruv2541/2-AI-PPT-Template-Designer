from typing import List
from uuid import UUID
from app.repositories.base import BaseRepository
from app.models.slide import Slide
from app import db


class SlideRepository(BaseRepository[Slide]):
    def __init__(self):
        super().__init__(Slide)

    def get_by_presentation_id(self, presentation_id: UUID) -> List[Slide]:
        return (
            db.session.query(Slide)
            .filter_by(presentation_id=presentation_id)
            .order_by(Slide.order_index)
            .all()
        )
