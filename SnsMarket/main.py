from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers import items, orders
from models.items import Item
from models.markets import Market
from models.orders import Order
from models.users import User
from exceptions import exceptions

app = FastAPI(
    title="SnsMarket",
    description="거래하기 안전한 SNS 마켓 API 문서"
)
app.include_router(items.router)
app.include_router(orders.router)


@app.exception_handler(exceptions.BadRequestException)
def bad_request_exception_handler(
    request: Request, exc: exceptions.BadRequestException
):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


@app.exception_handler(exceptions.NotFoundException)
def not_found_exception_handler(request: Request, exc: exceptions.NotFoundException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})
