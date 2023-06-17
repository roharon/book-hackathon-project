from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    orders = relationship("Order", back_populates="user")
