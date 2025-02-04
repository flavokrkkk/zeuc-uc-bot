from fastapi import WebSocket


class WebsocketManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, order_id: str, websocket: WebSocket):
        await websocket.accept() 
        self.connections[order_id] = websocket

    async def send_message(self, order_id: str, message: dict[str, str], event: str):
        connection = self.connections.get(order_id)
        if connection:
            await connection.send_json({**message, "event": event})

    async def disconnect(self, order_id: str):
        connection = self.connections.pop(order_id, None)
        if connection:
            await connection.close()
