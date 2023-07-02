from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref

from db.base_class import Base


class MenuImage(Base):
    __tablename__ = "menu_images"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    image_url = Column(String, index=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
    )

    menu = relationship("Menu", backref=backref("menu_images"))
