from fastapi import APIRouter

router = APIRouter()


@router.get("/markets")
def read_markets():
    return "aa"

# https://fastapi.tiangolo.com/tutorial/bigger-applications/