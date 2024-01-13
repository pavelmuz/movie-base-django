from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
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
            messages.error(
                request, 'Пользователь с таким именем не существует')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли')
            return redirect('movies')
        messages.error(request, 'Неверный пароль, попробуйте снова')

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
            return redirect('edit_profile')
        messages.error(request, 'Ошибка при регистрации, попробуйте еще раз')

    context = {'page': 'register', 'form': form}
    return render(request, 'users/login-register.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('login')


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    movies = Movie.objects.filter(owner=profile).order_by('-user_rating')
    context = {
        'profile': profile,
        'movies': movies
    }
    return render(request, 'users/account.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    movies = Movie.objects.filter(owner=profile).order_by('-user_rating')
    context = {
        'profile': profile,
        'movies': movies
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно изменен')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/edit-profile.html', context)


@login_required(login_url='login')
def delete_account(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Аккаунт успешно удален')
        return redirect('login')

    return render(request, 'users/delete-account.html')


def search_users(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.all().exclude(
            user=request.user).order_by('username')
    else:
        profiles = Profile.objects.all().order_by('username')
    context = {
        'profiles': profiles
    }
    return render(request, 'users/search-profiles.html', context)
