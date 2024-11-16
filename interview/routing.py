from django.urls import path
from interview import consumers  # Replace with your actual app name

websocket_urlpatterns = [
    path("ws/some_path/", consumers.InterviewConsumer.as_asgi()),
]
