from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_msg/', views.get_msg, name='get_msg'),
    path('get_group_msg/', views.get_group_msg, name='get_group_msg'),
    path('block', views.block_friend, name='block_friend'),
    path('search_people', views.search_people, name='search_people'),
    # path('add_msg', views.add_msg, name='add_msg')

    path('profile', views.profile, name='profile'),
    path('about', views.About.as_view()),
]