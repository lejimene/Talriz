from channels.generic.websocket import WebsocketConsumer
import json

Clients = {}
class NotificationConsumer(WebsocketConsumer):

    def connect(self):
        username = "None"
        if self.scope["user"].is_authenticated:
            username = self.scope["user"].username 

        if self not in Clients: 
            Clients[self] = username
        self.accept()

    def disconnect(self, close_code):
        if self in Clients: 
            Clients.pop(self)
        

    def receive(self, text_data): 
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        buyer = text_data_json.get('buyer', '')
        seller = text_data_json.get('seller', '')
        id = text_data_json.get('id', '')

        Likes = text_data_json.get('Likes', '')
        item_id = text_data_json.get('item_id', '')

        if Likes == "":
            for socket in Clients: 
                user = Clients[socket]
                if user == buyer or user == seller :
                    socket.send(text_data = json.dumps({
                        'message': message,
                        'buyer': buyer,
                        'seller': seller,
                        'id': id
                    }))
        else :
            for socket in Clients: 
                socket.send(text_data = json.dumps({
                'Likes': Likes,
                'item_id': item_id,
                'username':Clients[socket]
                }))

       
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

# This probably should goto the backend