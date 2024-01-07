from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'username', 'birthday', 'profile_image', 'email']

        labels = {
            'name': 'Полное имя',
            'username': 'Имя пользователя',
            'birthday': 'Дата рождения',
            'profile_image': 'Аватар',
            'email': 'Электронная почта'
        }
