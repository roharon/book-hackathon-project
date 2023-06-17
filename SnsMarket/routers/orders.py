from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from services.orders import order_exists, order_item
from schemas.orders import OrderExists, Order, SingleOrder
from models.users import User
import json

from database import get_db
from services.auth import current_user

router = APIRouter()


@router.get(
    "/orders/exists", dependencies=[Depends(HTTPBearer())], response_model=OrderExists
)
def list_items(
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    return JSONResponse(status_code=200, content={"data": order_exists(db, user.id)})


@router.post("/order", dependencies=[Depends(HTTPBearer())], response_model=SingleOrder)
def order(
    item_id: int,
    quantity: int,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    result = order_item(db, user.id, item_id, quantity)
    return JSONResponse(status_code=201, content={"data": result})
