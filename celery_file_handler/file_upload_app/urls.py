from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='ui-index'),
    path('upload_ui/', views.ui_file_upload_view, name='ui-file-upload'),
    path('upload/', views.api_file_upload_view, name='api-file-upload'),
    path('files_ui/', views.ui_file_list_view, name='ui-file-list'),
    path('files/', views.api_file_list_view, name='api-file-list'),
]
