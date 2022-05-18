from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from django.db.models import Q

from users.models import FriendRequest, FriendList, Room


class FriendRequestWSConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        data = {}
        all_is_ok = False
        if text_data_json['type'] == 'friend_request':
            to_user_id = int(text_data_json['to_user_id'])
            if self.user.id != to_user_id:  # user cannot send friend request to himself
                check_if_friends = FriendList.objects.filter(user=self.user, friend_id=to_user_id)
                check_data_friend_request = FriendRequest.objects.filter((Q(from_user_id=self.user.id, to_user_id=to_user_id) | Q(from_user_id=to_user_id, to_user_id=self.user.id)) & ~Q(status=False))
                if not check_data_friend_request and not check_if_friends:
                    new_friend_request = FriendRequest.objects.create(from_user_id=self.user.id, to_user_id=to_user_id)
                    data = {
                        'type': 'friend_request',
                        'from_user_id': self.user.id,
                        'from_user_name': self.user.username,
                        'to_user_id': to_user_id,
                    }
                    all_is_ok = True
        elif text_data_json['type'] == 'friend_request_reaction':
            from django.utils import timezone

            from_user_id = self.user.id
            status = text_data_json['status'] if text_data_json['status'] == True else False
            request_from_user_id = text_data_json['request_from_user_id']

            response_swal_msg = 'Friend request was declined'
            request_swal_msg = self.user.username + ' declined your friend request'
            try:
                friend_request = FriendRequest.objects.get(from_user_id=request_from_user_id, to_user_id=from_user_id, status__isnull=True)
                friend_request.status = status
                friend_request.reaction_date = timezone.now()
                friend_request.save()
                if status:  # if friend request was accepted then do insert to table FriendList and Room
                    room_id = Room.objects.create()
                    FriendList.objects.create(user_id=from_user_id, friend_id=request_from_user_id, room_id=room_id)
                    FriendList.objects.create(user_id=request_from_user_id, friend_id=from_user_id, room_id=room_id)

                    response_swal_msg = 'Friend request was accepted'
                    request_swal_msg = self.user.username + ' accepted your friend request'

                all_is_ok = True
                data = {
                    'type': 'friend_request_reaction',
                    'status': status,
                    'response_swal_msg': response_swal_msg,
                    'request_swal_msg': request_swal_msg,
                    'request_from_user_id':request_from_user_id,
                    'response_from_user_id': from_user_id,
                    'response_from_user_name': self.user.username,
                }
            except:
                pass

        if all_is_ok:
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                data
            )

    def friend_request(self, event):
        type = event['type']
        from_user_id = event['from_user_id']
        from_user_name = event['from_user_name']
        to_user_id = event['to_user_id']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': type,
            'from_user_id': from_user_id,
            'from_user_name': from_user_name,
            'to_user_id': to_user_id,
        }))

    def friend_request_reaction(self, event):
        type = event['type']
        status = event['status']
        response_swal_msg = event['response_swal_msg']
        request_swal_msg = event['request_swal_msg']
        request_from_user_id = event['request_from_user_id']
        response_from_user_id = event['response_from_user_id']
        response_from_user_name = event['response_from_user_name']

        self.send(text_data=json.dumps({
            'type': type,
            'status': status,
            'response_swal_msg': response_swal_msg,
            'request_swal_msg': request_swal_msg,
            'request_from_user_id': request_from_user_id,
            'response_from_user_id': response_from_user_id,
            'response_from_user_name': response_from_user_name,
        }))