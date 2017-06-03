# coding: utf-8

from django.conf.urls import url
from MediCare.chat import views


urlpatterns = [
    url(r'^receive/$', views.receive, name='receive'),
    url(r'^(?P<username>[^/]+)/$', views.messages, name='messages'),
]
