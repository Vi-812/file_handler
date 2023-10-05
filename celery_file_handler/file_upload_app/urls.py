from django.urls import path
from . import views


urlpatterns = [
    path('upload/', views.file_upload_view, name='file-upload'),
    path('files/', views.file_list_view, name='file-list'),
]
