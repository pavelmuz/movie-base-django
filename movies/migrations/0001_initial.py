# Generated by Django 5.0 on 2023-12-31 14:21

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('release_year', models.IntegerField()),
                ('user_rating', models.FloatField()),
                ('user_review', models.TextField(blank=True, max_length=500, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('poster_url', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name=uuid.uuid4)),
            ],
        ),
    ]
