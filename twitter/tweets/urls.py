from django.conf.urls import patterns, include, url

from rest_framework import routers

import tweets.views as views


router = routers.SimpleRouter()

router.register(r'tweets', views.TweetViewSet)
router.register(r'twitterusers', views.TwitterUserViewSet)

urlpatterns = patterns(
    'tweets.views',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^home$', 'home', name='home'),
)

urlpatterns += patterns('', url(r'^rest/', include(router.urls)))