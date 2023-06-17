from sqlalchemy.orm import sessionmaker

from database import engine
from models.items import Item
from models.markets import Market
from models.orders import Order
from models.users import User
from datetime import datetime

Item.__table__.create(bind=engine, checkfirst=True)
Market.__table__.create(bind=engine, checkfirst=True)
Order.__table__.create(bind=engine, checkfirst=True)
User.__table__.create(bind=engine, checkfirst=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

market = Market(name="첫번째 가게", certificated=True)
item = Item(name="연필", price="100", quantity="5", market_id=market.id)
user = User(name="노아론")

db = SessionLocal()
db.add(market)
db.add(item)
db.add(user)
db.commit()
