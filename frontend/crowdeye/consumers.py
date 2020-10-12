import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer




"""
How this works:
Each client (web browser page, electron instance...) is a `channel`. Each `channel`
has its own `Consumer` attached to it  
A channel can be a part of multiple groups, here, we have one group per camera  
A Consumer receives messages from `receive_json` and can decide to send a response back 
using `self.send_json` (sends a response only to the client) or broadcast a message to an entire 
group with `self.channel_layer.group_send` providing a groupname and a type. Each consumer should  
implement a function that matches the type an, in the function, send a message to its client.
"""
class CameraConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['camera']
        self.room_group_name = 'cam_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


        await self.send_json(
            {
                "status": "CONNECTED"
            })

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Received data from client (Sort of useless for now)
    async def receive_json(self, data):
        print(data)

        # # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat.message',
        #         'message': data
        #     }
        # )

    # Receive message from room group
    async def camera_data(self, event):
        data = event['message']

        # Send message to WebSocket
        await self.send_json({
            'data': data
        })
