from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship

from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    market_id = Column(Integer, ForeignKey("markets.id"), index=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.utc_timestamp(),
        onupdate=func.utc_timestamp(),
    )

    market = relationship("Market", back_populates="items")
