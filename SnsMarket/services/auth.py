from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from models.users import User
from database import get_db

user_map = {"aaaa": 1, "bbbb": 2}


def current_user(req: Request, db: Session = Depends(get_db)):
    token = req.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        raise HTTPException(status_code=401)

    user_id = user_map.get(token.split("Bearer ")[1])

    if user_id is None:
        raise HTTPException(status_code=401)

    user = db.query(User).get(user_id)
    return user
