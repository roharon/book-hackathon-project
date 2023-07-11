import uvicorn
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from api.api import api_router
from db.init_db import init_db
from db.session import SessionLocal

app = FastAPI(
    title="학생 식당 메뉴 API",
)
app.include_router(api_router)


@app.on_event("startup")
def db_initialize():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(BASE_DIR, ".env"))

    db = SessionLocal()
    init_db(db)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
