# project/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from users import consumers
  # Import WebSocket URL patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('login/', user_views.login_view, name='login'),
    # path('rfid_prompt/', user_views.rfid_prompt, name='rfid_prompt'),
    # path('test/', user_views.send_to_esp32, name='send_to_esp32'),  # Uncomment if needed
    path('', include('users.urls')),  # Include app-specific URL patterns
]
websocket_urlpatterns = [
    re_path(r'ws/rfid/', consumers.RFIDConsumer.as_asgi()),
]
# Include WebSocket URL patterns from users.urls

