import uuid

from django.db import models
from django.contrib.auth.models import User


class SiteUser(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE, related_name='siteuser')
    last_seen = models.DateTimeField(auto_now_add=True)
    is_online = models.BooleanField(default=False)
    is_private = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.user.username

class FriendList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fl_u')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fl_f')
    room_id = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='fl_room_id')
    had_blocked = models.BooleanField(default=False)
    insert_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='req_from')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='req_to')
    send_date = models.DateTimeField(auto_now_add=True)
    reaction_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(null=True)

    def __str__(self):
        return self.from_user.username


class Room(models.Model):
    room_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    insert_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.room_id}'
