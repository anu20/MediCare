from django.shortcuts import render

from django.conf.urls import url

from MediCare.products import views

urlpatterns = [
    url(r'^$', views.products_all, name='products_all'),
    url(r'^product_categories/$', views.products_all, name='products_all'),
    url(r'^(?P<slug>[\w-]+)/$', views.product, name='product'),
    url(r'^(\d+)/$', views.product, name='product'),
]
