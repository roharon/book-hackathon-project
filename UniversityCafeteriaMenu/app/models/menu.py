from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref

from db.base_class import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    cafeteria_id = Column(Integer, ForeignKey("cafeterias.id"))
    description = Column(String, index=True)
    price = Column(Integer)
    provides_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
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

    cafeteria = relationship("Cafeteria", backref=backref("menus"))
