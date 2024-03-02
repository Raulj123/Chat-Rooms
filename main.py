from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from db import create_schema, create_room
from typing import Dict, List
from collections import defaultdict

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_schema()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
       
    def disconnect(self, websocket: WebSocket, room_id: int):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, rooom_id: int):
       if rooom_id in self.active_connections:
           for connection in self.active_connections[rooom_id]:
               await connection.send_text(message)
    
    async def num_of_users(self, room_id: int) -> int:
        if room_id in self.active_connections:
            return len(self.active_connections[room_id])
        else:
            return 0 
           
manager = ConnectionManager()

@app.post("/create_room/{room_id}")
async def create_room_end(room_id: int):
    create_room(room_id)
    manager.active_connections[room_id] = []
    print(manager.active_connections)
    return {"roomID": room_id}

@app.websocket("/join_room/{room_id}")
async def join_room(websocket: WebSocket, room_id: int):
    if room_id not in manager.active_connections:
        await websocket.close(code=1000)
        return 
    await manager.connect(websocket, room_id)
    print(manager.active_connections)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)

@app.get("/users/{room_id}")
async def get_users(room_id: int):
     return {"num_people": await manager.num_of_users(room_id)}