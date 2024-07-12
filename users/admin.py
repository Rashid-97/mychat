from django.contrib import admin

from .models import SiteUser, FriendList, FriendRequest, Room


class SiteUserAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in SiteUser._meta.get_fields()]
    list_display = ('id','user','last_seen','is_online','is_private')
    list_display_links = ('last_seen','is_online','is_private')
    # exclude = ('is_online',)

class FriendListAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FriendList._meta.get_fields()]

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FriendRequest._meta.get_fields()]

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'insert_date')


admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(FriendList, FriendListAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Room, RoomAdmin)