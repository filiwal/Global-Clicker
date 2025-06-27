from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

counter = 0
connections = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global counter
    await websocket.accept()
    connections.add(websocket)
    try:
        await websocket.send_json({"counter": counter})
        while True:
            data = await websocket.receive_json()
            if data.get("action") == "increment":
                counter += 1
            elif data.get("action") == "decrement":
                counter -= 1
            elif data.get("action") == "increment100":
                counter += 100
            elif data.get("action") == "decrement100":
                counter -= 100
            # Broadcast the updated counter to all connected clients
            for conn in connections:
                await conn.send_json({"counter": counter})
    except WebSocketDisconnect:
        connections.remove(websocket)