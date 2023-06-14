from fastapi import APIRouter

router = APIRouter()


@router.get("/orders")
def read_orders():
    return "aa"

# https://fastapi.tiangolo.com/tutorial/bigger-applications/