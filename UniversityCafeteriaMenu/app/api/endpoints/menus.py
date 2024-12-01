from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.crud_menus import menu
from crud.crud_universities import university
from crud.crud_cafeterias import cafeteria
from schemas.menu import MenuImageUpload
from models.menu import Menu
from models.cafeteria import Cafeteria
from models.university import University
from api.deps import get_db

router = APIRouter()


@router.get("/universities/{university_id}/cafeterias/menus")
def list_menus(university_id: int, db: Session = Depends(get_db)):
    university_datum = university.get(db, id=university_id)
    if not university_datum:
        raise HTTPException(status_code=404, detail="해당하는 대학이 없습니다")

    result = menu.get_menus_with_cafeteria_by_university_id(db, university_id=university_datum.id)
    return result


@router.post("/menus/{menu_id}/image", status_code=201)
def create_menu_image(menu_id: int, menu_image: MenuImageUpload, db: Session = Depends(get_db)):
    menu_datum = menu.get(db, id=menu_id)
    if not menu_datum:
        raise HTTPException(status_code=404, detail="해당하는 메뉴가 없습니다")

    result = menu.add_menu_image(db, menu_id=menu_datum.id, image_url=menu_image.image_url)
    return


@router.post("/menus/event")
def create_menus(db: Session = Depends(get_db)):
   menu = Menu(description="비빔밥\n핫도그", price="3000", cafeteria_id=1)
    # TODO: 크롤링하여 메뉴 가져오기
   db.add(menu)
   db.commit()
