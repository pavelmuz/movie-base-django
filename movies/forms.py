from django.forms import ModelForm
from .models import Movie


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['user_review', 'user_rating']

        labels = {
            'user_review': 'Ваш обзор:',
            'user_rating': 'Ваша оценка:'
        }

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control my-2',
                'style': 'color: #0b666a;'
            })

        self.fields['user_review'].widget.attrs.update({
            'rows': '4'
        })
