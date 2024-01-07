from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('account/', views.user_account, name='account'),
    path('search/', views.search_users, name='search'),
    path('edit-profile/', views.edit_account, name='edit_profile'),
    path('delete-profile', views.delete_account, name='delete-profile'),
]
