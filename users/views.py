from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from movies.models import Movie
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile

# Create your views here.


def login_user(request):
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


def register_user(request):
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


def logout_user(request):
    logout(request)
    return redirect('login')


def user_account(request):
    profile = request.user.profile
    movies = Movie.objects.filter(owner=profile)
    context = {
        'profile': profile,
        'movies': movies
    }
    return render(request, 'users/account.html', context)


def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/edit-profile.html', context)


def delete_account(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile.delete()
        return redirect('login')

    return render(request, 'users/delete-account.html')


def search_users(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/search-profiles.html', context)
