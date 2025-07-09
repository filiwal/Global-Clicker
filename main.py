import time
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

RATE_LIMIT = 7  # max messages per second
RATE_PERIOD = 1  # seconds

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global counter
    money = 0
    await websocket.accept()
    connections.add(websocket)
    timestamps = []
    try:
        await websocket.send_json({"counter": counter, "money": money})
        while True:
            now = time.time()
            # Remove timestamps older than RATE_PERIOD
            timestamps[:] = [t for t in timestamps if now - t < RATE_PERIOD]
            if len(timestamps) >= RATE_LIMIT:
                await websocket.send_json({"error": "Rate limit exceeded"})
                continue
            timestamps.append(now)

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