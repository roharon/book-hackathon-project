from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.university import University
from schemas.university import UniversityInDBBase, UniversityCreate, UniversityUpdate


class CRUDUniversity(CRUDBase[UniversityInDBBase, UniversityCreate, UniversityUpdate]):
    def get_university(self, db: Session, *, id: int) -> UniversityInDBBase:
        return db.query(self.model).filter(University.id == id).first()


university = CRUDUniversity(University)
