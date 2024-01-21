from django.urls import path
from . import views

urlpatterns = [
    path('', views.chats, name='chats'),
    path('chat/<str:pk>/', views.chat, name='chat-details')
]
