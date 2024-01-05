from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect('movies')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            print("Username doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('movies')
        print('Username OR password is incorrect')

    context = {'page': 'login'}
    return render(request, 'users/login-register.html', context)


def register_view(request):
    context = {'page': 'register'}
    return render(request, 'users/login-register.html', context)


def logout_view(request):
    logout(request)
    return redirect('movies')
