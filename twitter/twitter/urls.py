from django.conf.urls import patterns, include, url
from django.contrib import admin

import tweets.views as views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^site/', include('tweets.urls')),
)
