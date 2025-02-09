from django.urls import path
from django.urls import re_path
from .consumers import KanbanConsumer

websocket_urlpatterns = [
    path('ws/kanban/', KanbanConsumer.as_asgi()),
     # path("ws/kanban/<int:lead_id>/", KanbanConsumer.as_asgi()),
     re_path(r"ws/kanban/(?P<lead_id>\d+)/$", KanbanConsumer.as_asgi()),
]
