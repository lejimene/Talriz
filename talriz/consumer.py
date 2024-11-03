class Consummer(AsyncWebsocketConsumer):
    async def connect(self):
        self.accept()

    async def receive(self, text_data):
        await self.send(text_data)

    async def disconnect(self, close_code):
        pass

# This probably should goto the backend