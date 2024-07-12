from django.conf.urls import url
from django.urls import path
from .consumers import WSConsumer, GroupWSConsumer
from .friend_request_consumers import FriendRequestWSConsumer

ws_urlpatterns = [
    url('ws/chat/(?P<room_name>\w+)', WSConsumer.as_asgi()), # for chat with friends
    url('ws/group_chat/(?P<room_name>\w+)', GroupWSConsumer.as_asgi()), # for chat in groups
    url('ws/request_friend/(?P<room_name>\w+)', FriendRequestWSConsumer.as_asgi()), # for chat in groups
]