from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship

from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    market_id = Column(Integer, ForeignKey("markets.id"), nullable=False)

    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
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

    market = relationship("Market", back_populates="items")
    order = relationship("Order", back_populates="items")
