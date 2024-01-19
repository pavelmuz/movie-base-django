from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('delete/<str:pk>', views.delete_notification, name='delete_notification')
]
