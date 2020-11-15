# _*_ coding: utf-8 _*_
# @Author: smiles
# @Time  : 2020/11/15 20:57
# @File  : urls.py

from django.urls import path

from .views import index


urlpatterns = [
    path('', index),
]