import os
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user="postgres",
            password="password",
            host="127.0.0.1:5432",
            # host="db",
            path="/app"
            # user=values.get("POSTGRES_USER"),
            # password=values.get("POSTGRES_PASSWORD"),
            # host=values.get("POSTGRES_SERVER"),
            # path=values.get("POSTGRES_DB"),
        )


settings = Settings()
