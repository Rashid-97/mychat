from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from users.models import SiteUser, FriendList
from .models import Message, UserGroup, GroupMessage


class WSConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        # data = {
        #     'logged_user_id': self.user.id
        # }
        # self.send(json.dumps(data))

    def disconnect(self, close_code):
        # Leave room group
        data = {
            'type': 'user_logged_in_out',
            'logged_type': 0,
            'logged_user_id': self.user.id
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            data
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = {}
        if text_data_json['type'] == 'is_typing':
            data = {
                'type': 'chat_typing',
                'from_user': self.user.id,
            }
        elif text_data_json['type'] == 'is_msg' and 'msg' in text_data_json and 'to_user' in text_data_json:
            if text_data_json['msg'] is not None and text_data_json['to_user'] is not None:
                message = text_data_json['msg']
                friend_id = text_data_json['to_user']
                to_user = SiteUser.objects.get(user_id=friend_id).user
                from_user = self.user
                new_msg = Message()
                new_msg.text = message
                new_msg.from_user = from_user
                new_msg.to_user = to_user
                new_msg.save()
                data = {
                    'type': 'chat_message',
                    'message': message,
                    'to_user': to_user.id,
                    'from_user': from_user.id
                }

        elif text_data_json['type'] == 'is_user_logged_in_out':
            data = {
                'type': 'user_logged_in_out',
                'logged_type': text_data_json['logged_type'],
                'logged_user_id': self.user.id
            }

        elif text_data_json['type'] == 'is_msg_readed':
            msg_from_user_id = text_data_json['msg_from_user_id']
            check_if_friends = FriendList.objects.filter(user_id=self.user.id, friend_id=msg_from_user_id, had_blocked=False)
            if check_if_friends:
                message = Message.objects.filter(from_user_id=msg_from_user_id, to_user=self.user, status=True, is_read=False).update(is_read=True)
                if message:
                    data = {
                        'type': 'msg_readed',
                        'success': True
                    }
                else:
                    data = {
                        'type': 'msg_readed',
                        'success': False
                    }
            else:
                pass

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            data
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        to_user = event['to_user']
        from_user = event['from_user']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'msg',
            'message': message,
            'to_user': to_user,
            'from_user': from_user
        }))

    def chat_typing(self, event):
        from_user = event['from_user']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'typing',
            'from_user': from_user
        }))

    def user_logged_in_out(self, event):
        logged_user_id = event['logged_user_id']
        logged_type = event['logged_type']

        self.send(text_data=json.dumps({
            'type': 'user_logged_in_out',
            'logged_type': logged_type,
            'logged_user_id': logged_user_id
        }))

    def msg_readed(self, event):
        success = event['success'] # if there are any markable messages to send friend
        if success:
            self.send(text_data=json.dumps({
                'type': 'msg_readed',
                'for_user_id': self.user.id
            }))


class GroupWSConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        data = {}

        if text_data_json['type'] == 'is_msg':
            msg = text_data_json['msg']
            group_id = text_data_json['group_id']
            user_id = text_data_json['from_user']
            check_user = UserGroup.objects.filter(group_id=group_id, member_id=user_id)
            if check_user:
                group_msg = GroupMessage()
                group_msg.text = msg
                group_msg.group_id = group_id
                group_msg.who_sent_id = user_id
                group_msg.save()
                sent_date = GroupMessage.objects.values('sent_date').filter(id=group_msg.id)
                data = {
                    'type': 'group_chat_message',
                    'msg': msg,
                    'sent_date': str(sent_date[0]['sent_date']),
                    'group_id': group_id,
                    'from_user': user_id
                }

        elif text_data_json['type'] == 'is_typing':
            from_user = SiteUser.objects.get(user_id=self.user.id)
            group_id = text_data_json['group_id']
            data = {
                'type': 'group_chat_typing',
                'group_id': group_id,
                'from_user': from_user.user.username,
                'from_user_id': from_user.user.id,
            }
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            data
        )

    def group_chat_message(self, event):
        msg = event['msg']
        sent_date = event['sent_date']
        from_user = event['from_user']
        group_id = event['group_id']

        self.send(text_data=json.dumps({
            'type': 'group_msg',
            'msg': msg,
            'sent_date': sent_date,
            'group_id': group_id,
            'from_user': from_user
        }))

    def group_chat_typing(self, event):
        from_user = event['from_user']
        from_user_id = event['from_user_id']
        group_id = event['group_id']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'group_typing',
            'from_user': from_user,
            'from_user_id': from_user_id,
            'group_id': group_id
        }))