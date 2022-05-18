from django.db import models

from django.contrib.auth.models import User
# from fernet_fields import EncryptedTextField

class Message(models.Model):
    text = models.TextField()
    # enc_text = EncryptedTextField()
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_from')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_to')
    is_read = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    sent_date = models.DateTimeField(auto_now_add=True)
    deleted_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.text


class Group(models.Model):
    name = models.CharField(max_length=100)
    who_created = models.ForeignKey(User, on_delete=models.CASCADE, related_name='g_who_created')
    who_deleted = models.ForeignKey(User, on_delete=models.CASCADE, related_name='g_who_deleted', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='ug_group')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ug_user')
    is_admin = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True)
    leave_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.group.name

class GroupMessage(models.Model):
    text = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    who_sent = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)
    deleted_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.text