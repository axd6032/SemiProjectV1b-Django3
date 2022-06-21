from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
    path('myinfo/', views.myinfo, name='myinfo')
]