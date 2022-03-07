import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class VideoConsumer(WebsocketConsumer):
    def connect(self):
        self.partner_id = self.scope['url_route']['kwargs']['partner_id']
        self.ecransPartner = 'ecran_%s' % self.partner_id

        
        async_to_sync(self.channel_layer.ecran_add)(
            self.ecransPartner,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
      
        async_to_sync(self.channel_layer.group_discard)(
            self.ecransPartner,
            self.channel_name
        )

    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

       
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
               
            }
        )

  
    def chat_message(self, event):
        message = event['message']
      

        self.send(text_data=json.dumps({
            'message': message,
          
        }))