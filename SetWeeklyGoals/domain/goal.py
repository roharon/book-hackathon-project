from sqlalchemy import String, Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Goal(base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    description = Column(String)
    resolved = Column(Boolean)
    year = Column(Integer)
    month = Column(Integer)
    week = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def as_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "resolved": self.resolved,
            "month": self.month,
            "week": self.week,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
