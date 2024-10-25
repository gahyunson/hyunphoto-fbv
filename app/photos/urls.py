from django.urls import path, include

from photos import views


app_name = 'photos'

urlpatterns = [
    # path('create/', views.createPhoto, name='create-photo')
    path('', views.photo_list, name='photos-list'),
    path('<int:photo_id>/', views.photo_detail, name='photo-detail'),
]