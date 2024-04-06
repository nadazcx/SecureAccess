from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
from .consumers import rfid_verified
from django.shortcuts import render


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Generate a new token for the user
            token, created = Token.objects.get_or_create(user=user)
            # Store the token key in the session for subsequent requests
            request.session['auth_token'] = token.key

            # Send the token to ESP32 device via WebSocket
            send_token_to_esp32(token.key)

            return redirect('rfid_prompt')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

def send_token_to_esp32(token):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
       'esp32_group',
        {
            'type': 'send_token_to_client',
            'token': token,
        }
    )
    logging.info('Token sent to ESP32')




def rfid_prompt(request):

    return render(request, 'rfid_prompt.html')




def success_view(request):
    def handle_rfid_verified(sender, **kwargs):
        user_id = kwargs['user_id']
        # Render success page with necessary data
        return render(request, 'success.html', {'user_id': user_id})

    # Connect the signal handler to the custom signal
    rfid_verified.connect(handle_rfid_verified)

    # Render waiting page initially
    return render(request, 'waiting.html')