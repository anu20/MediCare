"""MediCare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from MediCare.medicine import views as medicine_views
from MediCare.labs import views as labs_views
from MediCare.carts import views as carts_views
from MediCare.orders import views as orders_views
from MediCare.products import views as products_views
from MediCare.accounts import views as accounts_views
from MediCare.authentication import views as MediCare_auth_views
from chatterbot.ext.django_chatterbot import urls as chatterbot_urls
from MediCare.medicine import urls as medicine_urls
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', medicine_views.prescription , name='prescription'),
    url(r'^chat/', include('MediCare.chat.urls',namespace='chat')),
    url(r'^medicine/', include(medicine_urls)),
    url(r'^api/chatterbot/', include(chatterbot_urls, namespace='chatterbot')),
    url(r'^upload_picture/$', medicine_views.upload_picture,name='upload_picture'),
    url(r'^medicine/save_uploaded_picture/$', medicine_views.save_uploaded_picture,name='save_uploaded_picture'),
    url(r'^accounts/login/$',accounts_views.login_view, name='auth_login'),
    url(r'^accounts/logout/$',accounts_views.logout_view, name='auth_logout'),
    url(r'^accounts/register/$', accounts_views.registration_view, name='auth_register'),
    url(r'^accounts/address/add/$', accounts_views.add_user_address, name='add_user_address'),
    url(r'^carts/(?P<id>\d+)/$', carts_views.remove_from_cart, name='remove_from_cart'),
    url(r'^carts/(?P<slug>[\w-]+)/$', carts_views.add_to_cart, name='add_to_cart'),
    url(r'^cart/$', carts_views.view, name='cart'),
    url(r'^checkout/$', orders_views.checkout, name='checkout'),
    url(r'^orders/$', orders_views.orders, name='user_orders'),
    url(r'^labs/$', labs_views.labs,name='labs'),
    url(r'^labs/(?P<slug>[\w-]+)/$', labs_views.single, name='single'),
    url(r'^product_all/$', products_views.products_all, name='products_all'),
    url(r'^products_all/(?P<slug>[\w-]+)/$', products_views.product, name='product'),
    url(r'^ajax/add_user_address/$', accounts_views.add_user_address, name='ajax_add_user_address'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
