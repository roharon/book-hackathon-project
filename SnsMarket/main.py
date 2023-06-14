from fastapi import FastAPI
from routers import users, items, orders, markets

app = FastAPI()
app.include_router(users.router)
app.include_router(items.router)
app.include_router(orders.router)
app.include_router(markets.router)


@app.get("/")
def root():
    return {"message": "Hello, world!"}
