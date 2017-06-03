# coding: utf-8

from django.conf.urls import url
from chatterbot.ext.django_chatterbot import urls as chatterbot_urls
from MediCare.medicine import views

urlpatterns = [
    url(r'^post/$',views.post,name='post')
       
]
