from sqlalchemy.orm import Session

from models.items import Item
from models.markets import Market
from schemas.items import ItemCreate
from exceptions import exceptions


def fetch_items(db: Session, page: int, per: int, certificated_badge: bool = False):
    items_query = None
    if certificated_badge:
        items_query = (
            db.query(Item)
            .join(Item.market)
            .filter(Item.market_id == Market.id, Market.certificated == True)
        )
    else:
        items_query = db.query(Item)

    return items_query.offset(per * (page - 1)).limit(per).all()


def fetch_item(db: Session, id: int):
    item = db.query(Item).get(id)

    if item is None:
        raise exceptions.NotFoundException(message="상품이 존재하지 않습니다.")

    return item


def create_item(db: Session, item_create: ItemCreate):
    item = Item(**item_create.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
