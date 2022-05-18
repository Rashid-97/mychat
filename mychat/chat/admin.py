from django.contrib import admin

from chat.models import Message, Group, UserGroup, GroupMessage


class MessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Message._meta.get_fields()]


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'who_created', 'who_deleted', 'date_created', 'date_deleted', 'status')


class UserGroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserGroup._meta.get_fields()]


class GroupMessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GroupMessage._meta.get_fields()]


admin.site.register(Message, MessageAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(UserGroup, UserGroupAdmin)
admin.site.register(GroupMessage, GroupMessageAdmin)
