from fastapi import APIRouter

router = APIRouter()


@router.get("/users")
def read_users():
    return "aa"

# https://fastapi.tiangolo.com/tutorial/bigger-applications/