from fastapi import APIRouter

router = APIRouter()


@router.get("/items")
def read_items():
    return "aa"

# https://fastapi.tiangolo.com/tutorial/bigger-applications/