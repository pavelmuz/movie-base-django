from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']

        labels = {
            'username': 'Имя пользователя:',
            'email': 'Электронная почта:',
            'first_name': 'Полное имя:',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['password1'].label = 'Пароль:'
        self.fields['password2'].label = 'Подтвердите пароль:'

        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control my-2',
                'style': 'color: #0b666a;'
            })

            self.fields['password1'].widget.attrs.update({
                'type': 'password'
            })


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'name', 'birthday', 'email', 'profile_image']

        labels = {
            'name': 'Полное имя:',
            'username': 'Имя пользователя:',
            'birthday': 'Дата рождения:',
            'profile_image': 'Фото профиля:',
            'email': 'Электронная почта:'
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control my-2',
                'style': 'color: #0b666a;'
            })

        self.fields['email'].widget.attrs.update({
            'type': 'email'
        })

        self.fields['profile_image'].widget.attrs.update({
            'type': 'file'
        })
