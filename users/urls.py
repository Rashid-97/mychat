from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register', views.register_form, name='register_form'),
    path('adduser', views.adduser, name='adduser'),
    path('login', views.login_form, name='login_form'),
    path('auth_user', views.auth_user, name='auth_user'),
    path('logout', views.logout_form, name='logout_form'),
]
