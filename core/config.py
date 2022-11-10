from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    
    API_V1_STR = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:dev@localhost:5432/faculdade"
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True
    
    
settings = Settings()