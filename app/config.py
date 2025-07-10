from dotenv import load_dotenv
import os


SECRET_KEY=os.getenv("FASTAPI")
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = os.getenv("postgresql://postgres:123456@localhost/chatdb")