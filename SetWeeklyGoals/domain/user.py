from sqlalchemy import String, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
