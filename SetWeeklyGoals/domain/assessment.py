from sqlalchemy import String, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Assessment(base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    year = Column(Integer)
    month = Column(Integer)
    week = Column(Integer)
    content = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
