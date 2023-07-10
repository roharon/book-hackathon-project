from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.cafeteria import Cafeteria
from schemas.cafeteria import CafeteriaBase, CafeteriaCreate, CafeteriaUpdate


class CRUDCafeteria(CRUDBase[CafeteriaBase, CafeteriaCreate, CafeteriaUpdate]):
    def get_first_cafeteria(self, db: Session) -> CafeteriaBase:
        return db.query(self.model).first()


cafeteria = CRUDCafeteria(Cafeteria)
