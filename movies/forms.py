from django.forms import ModelForm
from .models import Movie, Comment


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


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        labels = {
            'body': 'Комментарий:'
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['body'].widget.attrs.update({
            'class': 'form-control my-2',
            'style': 'color: #0b666a;',
            'rows': '4'
        })
