from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

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
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('movies')
        print('Error during registration')

    context = {'page': 'register', 'form': form}
    return render(request, 'users/login-register.html', context)


def logout_view(request):
    logout(request)
    return redirect('movies')
