# coding: utf-8

from django.conf.urls import url

from MediCare.labs import views

urlpatterns = [
    url(r'^$', views.labs, name='labs'),
    url(r'^categories/$', views.all, name='all'),
    url(r'^(?P<slug>[\w-]+)/$', views.single, name='single'),
    url(r'^(\d+)/$', views.single, name='single'),
    url(r'^load/$', views.load, name='load'), 
]
