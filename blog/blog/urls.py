
from django.contrib import admin
from django.urls import path, re_path
from articles import views

urlpatterns = [
    re_path(r'^article/(?P<article_id>\d+)$', views.get_article, name='get_article'),
    path('', views.archive, name='archive'),
    path('admin/', admin.site.urls),
    path('article/new/', views.create_post, name='create_post'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
]