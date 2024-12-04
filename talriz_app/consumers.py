from channels.generic.websocket import WebsocketConsumer
import json

Clients = []
class NotificationConsumer(WebsocketConsumer):

    def connect(self):
        if self not in Clients: 
            Clients.append(self)
        self.accept()

    def disconnect(self, close_code):
        if self in Clients: 
            Clients.remove(self)
        

    def receive(self, text_data): 
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        username = text_data_json.get('username', '')
        for users in Clients[:]: 
            users.send(text_data = json.dumps({
                'message': message,
                'username': username
            }))

       
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

# This probably should goto the backend