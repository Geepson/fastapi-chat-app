from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
from .config import SECRET_KEY,ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session
import app.models as models

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str , hashed_password: str):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_table(data:str , expires_delta: timedelta =None):
    to_encode=data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db:Session, username:str , password:str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

    
