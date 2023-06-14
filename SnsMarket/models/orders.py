"""
id
userId
itemId
quantity
totalPrice
createdAt
updatedAt
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy import func
from sqlalchemy.orm import relationship

from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.utc_timestamp(),
        onupdate=func.utc_timestamp(),
    )

    user = relationship("User", back_populates="orders")
    item = relationship("Item", back_populates="orders")
