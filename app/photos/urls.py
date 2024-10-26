from django.urls import path

from photos import views


app_name = 'photos'

urlpatterns = [
    path('', views.photo_list, name='photos-list'),
    path('<int:photo_id>/', views.photo_detail, name='photo-detail'),
]
