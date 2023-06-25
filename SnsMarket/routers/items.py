from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.items import fetch_items, fetch_item
from schemas.items import ListItems, ShowItem

from database import get_db

router = APIRouter()


@router.get("/items", response_model=ListItems)
def list_items(
    page: int = 1,
    per: int = 12,
    certificated_badge: bool = False,
    db: Session = Depends(get_db),
):
    items = fetch_items(db, page, per, certificated_badge)

    return {"data": items}


@router.get("/items/{id}", response_model=ShowItem)
def show_item(id: int, db: Session = Depends(get_db)):
    item = fetch_item(db, id)

    return {"data": item}
