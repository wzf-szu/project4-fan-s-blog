from django.urls import path

from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('new/', views.new_post, name='new_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
]
