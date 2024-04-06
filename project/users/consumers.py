import asyncio
import random
import string
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.template.loader import render_to_string

from django.dispatch import Signal
from django.shortcuts import render

rfid_verified = Signal()






logger = logging.getLogger(__name__)

class RFIDConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('esp32_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Handle disconnection if needed

    async def receive(self, text_data):
        logger.info(f"Received data from client: {text_data}")
        data = json.loads(text_data)
        token = data.get('token')
        nuid = data.get('nuid')
        logger.info(f"Tokennnn: {token}, NnnUID: {nuid}")
        valid_user = await self.verify_user(token, nuid)
        if valid_user:
            logger.info("User verified successfully.")
            await self.send(text_data=json.dumps({'status': 'success'}))
            rfid_verified.send(sender=self.__class__, user_id=nuid)  # Trigger custom signal

        else:
            logger.warning("User verification failed.")
            await self.send(text_data=json.dumps({'status': 'fail'}))

    async def send_token_to_client(self, event):
        token = event['token']
        await self.send(text_data=json.dumps({'token': token}))
    

    @database_sync_to_async
    def get_token_async(self, token):

        from rest_framework.authtoken.models import Token

        try:
            token_entry = Token.objects.get(key=token)
            user_entry = token_entry.user
            logger.info(f"user_entry: {user_entry}")  # Check if user_entry is not None
            logger.info(f"the data is: {user_entry.cardId if user_entry else 'None'}")
            return user_entry.cardId if user_entry else None
        except Token.DoesNotExist:
            logger.error("Token not found in the database.")
            return None
        except Exception as e:
            logger.error(f"Error retrieving token: {e}")
            return None
        

        

    async def verify_user(self, token, nuid):
        from rest_framework.authtoken.models import Token
        try:
            # Use await with database_sync_to_async to handle the database operation asynchronously
            nn = await self.get_token_async(token)  # <-- Add await here
            
            if nn == nuid:
                return True
            else:
                return False
        except Token.DoesNotExist:
            return False
        except Exception as e:
            logger.error(f"Error verifying user: {e}")
            return False


