from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref

from db.base_class import Base


class Cafeteria(Base):
    __tablename__ = "cafeterias"

    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    name = Column(String, index=True)
    description = Column(String, index=True)
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

    university = relationship("University", backref=backref("cafeterias"))
