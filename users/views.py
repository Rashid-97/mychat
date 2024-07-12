from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import SiteUserLoginForm
from django.contrib.auth.models import User
from .models import SiteUser

from django.contrib.auth import authenticate, login, logout

def register_form(request):
    form = UserCreationForm()
    data = {
        'form':form
    }
    return render(request, 'users/register.html', data)

def adduser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.order_by('-id')[:1][0]
            last_user = User.objects.get(id=user.id)
            siteuser = SiteUser()
            siteuser.user = last_user
            siteuser.save()
            return redirect('users:login_form')
        else:
            return render(request, 'users/error.html', {'error':'Form is not Valid'})

    else:
        return render(request, 'users/error.html', {'error':'Request method error'})

def login_form(request):
    if request.user.is_authenticated:
        return redirect('chat:index')

    form = SiteUserLoginForm()
    data = {
        'form':form,
        'errors':''
    }
    return render(request, 'users/login.html', data)

def auth_user(request):
    if request.method == 'POST':
        form = SiteUserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                siteuser = SiteUser.objects.get(user=user)
                siteuser.is_online = True
                siteuser.save()
                return redirect('chat:index')
            else:
                return render(request, 'users/error.html', {'error': 'user is None'})
        return render(request, 'users/login.html', {'form':form, 'errors':form.errors})
    return render(request, 'users/error.html', {'error': 'Request method error'})

def logout_form(request):
    siteuser = SiteUser.objects.get(user=request.user)
    siteuser.is_online = False
    siteuser.save()
    logout(request)
    return redirect('users:login_form')