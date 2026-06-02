from typing import TypeVar, Generic, Type, List, Optional
from uuid import UUID
from app import db

T = TypeVar("T", bound=db.Model)


class BaseRepository(Generic[T]):
    def __init__(self, model_cls: Type[T]):
        self.model_cls = model_cls

    def get_by_id(self, id: UUID) -> Optional[T]:
        return db.session.get(self.model_cls, id)

    def get_all(self) -> List[T]:
        return db.session.query(self.model_cls).all()

    def create(self, entity: T) -> T:
        db.session.add(entity)
        db.session.commit()
        return entity

    def update(self, entity: T) -> T:
        db.session.merge(entity)
        db.session.commit()
        return entity

    def delete(self, entity: T) -> None:
        db.session.delete(entity)
        db.session.commit()
