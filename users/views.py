from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from movies.models import Movie
from movies.forms import CommentForm
from movies.utils import like_movie, unlike_movie, handle_liking_feed, add_comment
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile, Follow


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
    form = CommentForm()
    movies = Movie.objects.filter(owner=profile).order_by('-user_rating')
    handle_liking_feed(request, movies, 'account')
    add_comment(request, movies, 'account')
    context = {
        'profile': profile,
        'movies': movies,
        'form': form
    }
    return render(request, 'users/account.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    form = CommentForm()
    movies = Movie.objects.filter(owner=profile).order_by('-user_rating')

    if request.method == 'POST':
        for movie in movies:
            if f'movie-{movie.id}' in request.POST:
                if request.user.profile.id in movie.users_liked:
                    unlike_movie(request, movie)
                    return redirect('profile', profile.id)
                else:
                    like_movie(
                        profile=request.user.profile,
                        movie=movie
                    )
                    return redirect('profile', profile.id)
            else:
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.owner = request.user.profile
                    comment.movie = movie
                    comment.save()
                    return redirect('profile', profile.id)
        if f'follow-{profile.id}' in request.POST:
            Follow.objects.create(
                follower=request.user.profile,
                following=profile
            )
            return redirect('profile', profile.id)
        elif f'unfollow-{profile.id}' in request.POST:
            follow = Follow.objects.filter(
                follower=request.user.profile).filter(following=profile)
            follow.delete()
            return redirect('profile', profile.id)

    context = {
        'profile': profile,
        'movies': movies,
        'form': form
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

    return render(request, 'delete-template.html')


def search_users(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.all().exclude(
            user=request.user).order_by('username')
    else:
        profiles = Profile.objects.all().order_by('username')

    if request.method == 'POST':
        for profile in profiles:
            if f'follow-{profile.id}' in request.POST:
                Follow.objects.create(
                    follower=request.user.profile,
                    following=profile
                )
                return redirect('search')
            elif f'unfollow-{profile.id}' in request.POST:
                follow = Follow.objects.filter(
                    follower=request.user.profile).filter(following=profile)
                follow.delete()
                return redirect('search')

    context = {
        'profiles': profiles
    }
    return render(request, 'users/search-profiles.html', context)
