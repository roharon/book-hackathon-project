from sqlalchemy.orm import Session
from models.orders import Order
from models.items import Item
from exceptions import exceptions


def order_exists(db: Session, user_id: int):
    return bool(db.query(Order).filter_by(user_id=user_id).first())


def order_item(db: Session, user_id: int, item_id: int, quantity: int):
    if quantity < 1:
        raise exceptions.BadRequestException(message="수량은 1보다 작을 수 없습니다.")

    item = db.query(Item).get(item_id)

    if item is None:
        raise exceptions.BadRequestException(message="해당하는 상품이 없습니다")

    if item.quantity < quantity:
        raise exceptions.BadRequestException(message="상품의 잔여 수량이 구입하려는 양보다 작습니다.")

    transaction = db.get_transaction()

    order = Order(
        user_id=user_id,
        item_id=item.id,
        quantity=quantity,
        total_price=item.price * quantity,
    )

    db.add(order)
    item.quantity -= quantity
    db.commit()
    transaction.close()

    db.refresh(order)

    return {
        "id": order.id,
        "user_id": order.user_id,
        "item_id": order.item_id,
        "quantity": order.quantity,
        "total_price": order.total_price,
        "created_at": order.created_at.isoformat(),
        "updated_at": order.updated_at.isoformat(),
    }
