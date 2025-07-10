from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from auth import hash_password, create_access_table, authenticate_user
from dependencies import get_current_user, get_db,require_role
import models,schemas
from database import engine, Base
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError,jwt
from config import SECRET_KEY, ALGORITHM
from chat_manager import ConnectionManager
import json


app = FastAPI()
manager = ConnectionManager()

Base.metadata.create_all(bind=engine)

@app.post("/signup")
def signup(user_data:schemas.UserCreate, db:Session =Depends(get_db)):
    existing=db.query(models.User).filter(models.User.username==user_data.username).first()
    if existing:
        raise HTTPException(status_code=400,detail="Username already exists")
    
    new_user = models.User(
         username = user_data.username,
        password = hash_password(user_data.password),
        role = user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"User created"}

@app.post("/login",response_model=schemas.Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
    user = authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    token = create_access_table({"sub":user.username,"role":user.role})
    return {"access_token":token,"token_type":"bearer"}


@app.get("/admin",dependencies=[Depends(require_role("admin"))])
def only_admin():
    return {"message":"Welcome admin!"}

def decode_jwt_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket,room_id:int, token : str,db:Session=Depends(get_db)):
    payload = decode_jwt_token(token)
    if not payload:
        await websocket.close(code=1008)
        return
    
    username = payload.get("sub")
    user = db.query(models.User).filter(models.User.username==username).first()
    if not user:
        await websocket.close(code=1008)
        return
    await manager.connect(room_id,websocket)
    
    messages = db.query(models.Message).filter(models.Message.room_id==room_id).order_by(models.Message.timestamp.desc()).limit(10).all()
    
    for message in reversed(message):
        await websocket.send_text(f"[{message.sender.username}]{message.content}")
    
    try:
        while True:
            data = await websocket.receive_text()
            new_msg = models.Message(content=data,sender_is = user.id,room_id=room_id)
            db.add(new_msg)
            db.commit()
            await manager.broadcast(room_id,f"[{user.username}]{data}")
    except WebSocketDisconnect:
        manager.disconenct(room_id,websocket)
        
@app.post("/rooms")
def create_room(room_data:schemas.RoomCreate, db:Session=Depends(get_db)):
    existing=db.query(models.Room).filter(models.Room.name==room_data.name).first()
    if existing:
        raise HTTPException(status_code=400,detail="Room name already exists")
    room = models.Room(name=room_data.name)
    db.add(room)
    db.commit()
    return {"message":f"Room '{room.name}' created"}

