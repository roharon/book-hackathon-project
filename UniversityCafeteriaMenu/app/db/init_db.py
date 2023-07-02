from sqlalchemy.orm import Session

from db.session import engine, SessionLocal
from db.base_class import Base  # noqa: F401
from models.university import University
from models.cafeteria import Cafeteria
from models.menu import Menu
from models.menu_image import MenuImage


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    university = University(name="한국대학교")
    db.add(university)
    db.commit()

    cafeteria = Cafeteria(
        name="본관 학생식당", description="학생식당입니다.", university_id=university.id
    )
    db.add(cafeteria)
    db.commit()

    menu = Menu(
        description="비빔밥\n핫도그", price="3500", cafeteria_id=cafeteria.id
    )
    db.add(menu)
    db.commit()

    menu_image = MenuImage(image_url="https://www.google.com", menu_id=menu.id)
    db.add(menu_image)
    db.commit()
