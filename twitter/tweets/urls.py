from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required

from rest_framework import routers

import tweets.views as views


router = routers.SimpleRouter()

router.register(r'tweets', views.TweetViewSet)
router.register(r'twitterusers', views.TwitterUserViewSet)

urlpatterns = patterns(
    'tweets.views',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^home$', views.HomeView.as_view(), name='home'),
    url(r'^login/$', login,
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout,
        {'template_name': 'logout.html'}, name='logout'),
    url(r'^register/$', views.RegistrationURLView.as_view(), name='register'),
)

urlpatterns += patterns('', url(r'^rest/', include(router.urls)))
