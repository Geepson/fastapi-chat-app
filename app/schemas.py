from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password : str
    role : Optional[str] ="user"
    
class UserLogin(BaseModel):
    username :str
    password : str
    
class Token(BaseModel):
    access_token :str
    token_type : str
    
class MessageCreate(BaseModel):
    content : str
    
class RoomCreate(BaseModel):
    name:str
    
