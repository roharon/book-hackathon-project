from fastapi import APIRouter

from api.endpoints import menus

api_router = APIRouter()
api_router.include_router(menus.router, tags=["menus"])
