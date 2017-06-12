"""customer_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from uaa_client import urls as uaa_urls
from uaa_client import views as uaa_views

urlpatterns = [
    url(r'^django-admin/login', uaa_views.login, name='login'),
    url(r'^', include('customer_info.urls')),
    url(r'^auth/', include(uaa_urls)),
    url(r'^django-admin/', include(admin.site.urls)),
]

#urlpatterns.insert(0,url(r'^django-admin/login', uaa_views.login, name='login'))
