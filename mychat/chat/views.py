from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count, When, Value, Case, Q

from users.models import FriendList, SiteUser, FriendRequest
from chat.models import Message, UserGroup, GroupMessage


@login_required
def index(request):
    user = request.user
    friends = FriendList.objects.filter(user=user)
    not_readed_msgs = Message.objects.filter(is_read=False, to_user=user).values('from_user').annotate(count=Count('text')).order_by()
    notification_count = FriendRequest.objects.filter(to_user=user, status__isnull=True).count()
    friend_requests = None
    if notification_count == 0:
        notification_count = ''
    else:
        friend_requests = FriendRequest.objects.filter(to_user=user, status__isnull=True)

    user_groups = UserGroup.objects.filter(member=user)
    data = {
        'friends': friends,
        'not_readed_msgs': not_readed_msgs,
        'user_groups': user_groups,
        'notification_count': notification_count,
        'friend_requests': friend_requests
    }
    return render(request, 'chat/index.html', data)

@login_required
def get_msg(request):

    if request.method == 'POST' and request.is_ajax():

        user_id = request.user.id
        friend_id = request.POST.get('friend_id')
        sql_offset = int( request.POST.get('sql_offset') )
        sql_limit = sql_offset + 10
        # Message.objects.filter(from_user_id=friend_id, to_user_id=user_id, status=True, is_read=False).update(is_read=True)
        messages = Message.objects.filter( Q(from_user_id=user_id, to_user_id=friend_id, status=True) | Q(from_user_id=friend_id, to_user_id=user_id, status=True)).order_by('-sent_date')[sql_offset:sql_limit]
        messages = serializers.serialize('json', messages)
        data = {
            'msgs':messages
        }
        return JsonResponse(data)

@login_required
def get_group_msg(request):
    if request.method == 'POST' and request.is_ajax():
        group_id = request.POST.get('group_id')
        sql_offset = int( request.POST.get('sql_offset') )
        sql_limit = sql_offset + 10
        messages = GroupMessage.objects.values('deleted_date', 'group', 'sent_date', 'status', 'text', 'who_sent', from_user=F('who_sent__username') ).filter(group_id=group_id).order_by('-sent_date')[sql_offset:sql_limit]
        # messages = serializers.serialize('json', messages)
        messages = list(messages)
        data = {
            'data': messages
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Request method or type error!'})
    pass
# @login_required
# def add_msg(request):
#     friend_id = request.POST.get('friend_id')
#     if request.method == 'POST' and request.is_ajax():
#         if friend_id is not None and friend_id != '':
#             user = request.user
#             check_friend = FriendList.objects.get(friend_id=friend_id, user_id=user.id)
#             if check_friend is not None:
#                 friend = User.objects.get(id=friend_id)
#                 message = Message()
#                 message.from_user = user
#                 message.to_user = friend
#                 message.text = request.POST.get('msg')
#                 message.save()
#                 resp = {
#                     'success':True
#                 }
#                 return HttpResponse(json.dumps(resp), content_type="application/json")
#             else:
#                 data = {
#                     'resp': 'You are not friends'
#                 }
#                 return HttpResponse(json.dumps(data), content_type="application/json")
#         return HttpResponse(json.dumps({'': ''}), content_type="application/json")
#     return HttpResponse(json.dumps({'':''}), content_type="application/json")

@login_required
def block_friend(request):
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        friend_id = request.POST.get('friend_id')
        user = FriendList.objects.get(user=user, friend_id=friend_id)
        if user is not None:
            user.had_blocked = True
            user.save()
            data = {
                'success': True
            }
            return JsonResponse(data)
        return JsonResponse({'error': 'User Not Found'})
    return JsonResponse({'error': 'Request Type Error'})

@login_required
def search_people(request):
    if request.is_ajax:
        friends_id = FriendList.objects.filter(user=request.user).values('friend_id')
        users = SiteUser.objects.exclude(Q(user_id__in=friends_id) | Q(user_id=request.user.id)).annotate(username=F('user__username'), person_id=F('user__id')).values('person_id', 'username', 'is_online').order_by('username')
        users = list(users)
        return JsonResponse(users, safe=False)
    return JsonResponse({'error':'Request Type Error'})


@login_required
def profile(request):
    return render(request, 'chat/profile.html')

from django.views.generic import TemplateView
class About(TemplateView):
    template_name = 'chat/about.html'