import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time notifications.
    """
    
    async def connect(self):
        """
        Called when a client connects to the WebSocket.
        """
        self.user = self.scope["user"]
        
        # Check if the user is authenticated
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Use the user's ID to create a unique notification channel
        self.notification_group_name = f'notifications_{self.user.id}'
        
        # Join the group
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send a connection success message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to notification service'
        }))
    
    async def disconnect(self, close_code):
        """
        Called when a client disconnects from the WebSocket.
        """
        # Leave the group
        if hasattr(self, 'notification_group_name'):
            await self.channel_layer.group_discard(
                self.notification_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """
        Called when the server receives a message from the client.
        """
        # Parse the message
        data = json.loads(text_data)
        message_type = data.get('type', '')
        
        # Handle message acknowledgment
        if message_type == 'notification_received':
            notification_id = data.get('notification_id')
            if notification_id:
                # Optionally mark notification as delivered
                # await self.mark_notification_delivered(notification_id)
                pass
    
    async def send_notification(self, event):
        """
        Called when a notification is sent to the group.
        """
        # Send the notification to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))
    
    @database_sync_to_async
    def mark_notification_delivered(self, notification_id):
        """
        Mark a notification as delivered in the database.
        """
        # This could be implemented if we want to track when notifications are delivered
        pass