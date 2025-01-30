import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DeviceStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle new WebSocket connection"""
        await self.accept()
        self.device_ip = None

    async def receive(self, text_data):
        """Handle incoming messages from WebSocket"""
        data = json.loads(text_data)
        self.device_ip = data.get("device_ip")

        if not self.device_ip:
            await self.send(text_data=json.dumps({"error": "Missing device IP"}))
            return

        # Subscribe to the "device_status" group
        await self.channel_layer.group_add("device_status", self.channel_name)
        await self.send(text_data=json.dumps({"message": "Listening for updates..."}))

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if self.device_ip:
            await self.channel_layer.group_discard("device_status", self.channel_name)

    async def send_status_update(self, event):
        """Receive messages from Django API and forward them to the WebSocket client"""
        await self.send(text_data=json.dumps(event["data"]))
