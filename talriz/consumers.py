from channels.generic.websocket import WebsocketConsumer
import json

Clients = set()
class NotificationConsumer(WebsocketConsumer):
    
    def connect(self):
        Clients.add(self)
        self.accept()

    def disconnect(self, close_code):
        Clients.discard(self)
        

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        for users in Clients: 
            users.send(text_data = json.dumps({
                'message': message
            }))

       
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

# This probably should goto the backend