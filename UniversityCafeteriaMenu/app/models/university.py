from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship

from db.base_class import Base


class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
    )
