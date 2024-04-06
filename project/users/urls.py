# # users/urls.py

# from django.urls import path
# from .consumers import RFIDConsumer


from django.urls import path
from django.urls import re_path
from . import consumers
from .views import login_view, rfid_prompt;
urlpatterns = [
    path('login/', login_view, name='login'),
    path('rfid_prompt/',      rfid_prompt, name='rfid_prompt'),
    # path('test/', send_to_esp32, name='send_to_esp32'),  # Uncomment if needed
    
    path('login/', login_view, name='login'),
]
