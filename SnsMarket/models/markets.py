from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import func
from sqlalchemy.orm import relationship

from database import Base


class Market(Base):
    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    certificated = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    items = relationship("Item", back_populates="market")
