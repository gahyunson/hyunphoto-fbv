from django.urls import path, include

from photos import views


app_name = 'photos'

urlpatterns = [
    # path('create/', views.createPhoto, name='create-photo')
    path('', views.photo_view, name='photos-list')
]