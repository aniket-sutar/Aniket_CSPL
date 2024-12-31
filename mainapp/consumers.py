import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "notifications"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', 'No message received')
        
        if message:
            try:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "send_notification",
                        "message": f"New notification: {message}"
                    }
                )
            except Exception as e:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "send_notification",
                        "message": f"Error occurred: {str(e)}"
                    }
                )

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "notification": message
        })) 