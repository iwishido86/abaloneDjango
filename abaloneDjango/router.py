from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path('abalone/<str:username>/', consumers.abalone_consumer),
]
