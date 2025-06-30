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
money = 0
connections = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global counter, money
    await websocket.accept()
    connections.add(websocket)
    try:
        await websocket.send_json({"counter": counter, "money": money})
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
            elif data.get("action") == "increment-money":
                money += 1
            elif data.get("action") == "spend-money":
                amount = data.get("amount", 0)
                if money >= amount:
                    money -= amount
            # Broadcast updated values to all clients
            for conn in connections:
                await conn.send_json({"counter": counter, "money": money})
    except WebSocketDisconnect:
        connections.remove(websocket)