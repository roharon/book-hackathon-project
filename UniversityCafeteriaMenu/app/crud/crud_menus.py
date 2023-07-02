from sqlalchemy.orm import Session, joinedload

from crud.base import CRUDBase
from models.menu import Menu
from models.cafeteria import Cafeteria
from models.menu_image import MenuImage
from schemas.menu import MenuInDBBase, MenuCreate, MenuUpdate
from schemas.cafeteria import CafeteriaWithMenus


class CRUDMenu(CRUDBase[MenuInDBBase, MenuCreate, MenuUpdate]):
    def create_menu(
        self, db: Session, *, obj_in: MenuCreate, description: str, price: int
    ) -> MenuInDBBase:
        db_obj = Menu(description=description, price=price)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_menus_with_cafeteria_by_university_id(
        self, db: Session, *, university_id: int
    ) -> CafeteriaWithMenus:
        return (
            db.query(Cafeteria)
            .options(joinedload(Cafeteria.menus))
            .options(joinedload(Cafeteria.menus, Menu.menu_images))
            .filter(Cafeteria.university_id == university_id)
            .all()
        )

    def add_menu_image(self, db: Session, *, menu_id: int, image_url: str):
        menu_image = MenuImage(image_url=image_url, menu_id=menu_id)
        db.add(menu_image)
        db.commit()
        return db.refresh(menu_image)


menu = CRUDMenu(Menu)
