"""
URL mappings for the user API.
"""
from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('token/', views.create_token, name='token'),
    path('profile/', views.profile, name='profile'),
]