"""dcos_devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from alertinfos import views as alert_info_views
from resourceremain import views as resource_remain_views
from dcos_yarn import views as dcos_yarn_views

urlpatterns = [
    url(r'^$', alert_info_views.index),
    url(r'^get_ip', alert_info_views.get_ip),
    url(r'^get_rest_information', alert_info_views.get_table_information),
    url(r'^get_service_time', alert_info_views.get_service_time),
    url(r'^cluster_resource', resource_remain_views.cluster_resource),
    url(r'^dcos_yarn', dcos_yarn_views.dcos_yarn),
]