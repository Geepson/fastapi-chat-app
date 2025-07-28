from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL:str
    SECRET_KEY:str
    ALGORITHM:str   
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    
    class Config:
        env_file = ".env"

settings = Settings()



SECRET_KEY=os.getenv("FASTAPI")
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = os.getenv("postgresql://postgres:123456@localhost/chatdb")