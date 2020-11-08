from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('login1', views.login1),
]
