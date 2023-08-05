import os
from typing import List

from pydantic import BaseSettings

class Configs(BaseSettings):
    # base
    ENV: str = "dev"
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"
    PROJECT_NAME: str = "pdf_bot"

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # auth
    SECRET_KEY: str = "BASILISK"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
    ALGORITHM: str = "HS256"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # find query
    PAGE = 1
    PAGE_SIZE = 20
    ORDERING = "-id"

    class Config:
        case_sensitive = True


class TestConfigs(Configs):
    ENV: str = "test"


configs = Configs()