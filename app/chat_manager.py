from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        self.active_connections:Dict[int,List[WebSocket]]={}
    
    async def connect(self,room_id:int, websocket:WebSocket):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id]=[]
        self.active_connections[room_id].append(websocket)
    
    def disconenct(self,room_id:int,websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)
        if not self.active_connections[room_id]:
            del self.active_connections[room_id]
        
    async def send_personal_message(self,message:str,websocket:WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self,room_id:int,message:str):
        for connection in self.active_connections.get(room_id,[]):
            await connection.send_text(message)
        