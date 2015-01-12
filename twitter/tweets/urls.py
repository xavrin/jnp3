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
    '',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^home$', views.HomeView.as_view(), name='home'),
    url(r'^tweet_search$', views.TweetSearchView.as_view(), name='tweetSearch'),
    url(r'^login/$', login,
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout,
        {'template_name': 'logout.html'}, name='logout'),
    url(r'^create_tweet', login_required(views.TweetCreateView.as_view()),
        name='create_tweet'),
    url(r'^search', login_required(views.search),
        name='search'),
    url(r'^show_tweet/(?P<pk>\d+)/$', login_required(views.TweetDetailView.as_view()),
        name="show_tweet"),
    url(r'^user_profile/(?P<pk>\d+)/$', login_required(views.UserTweetsView.as_view()),
        name="profile"),
    url(r'^user_profile/(?P<pk>\d+)/followers/$', login_required(views.FollowersView.as_view()),
        name="followers"),
    url(r'^user_profile/(?P<pk>\d+)/followees/$', login_required(views.FolloweesView.as_view()),
        name="followees"),
    url(r'^register/$', views.RegistrationURLView.as_view(), name='register'),
    url(r'^user_profile/(?P<pk>\d+)/follow/$', login_required(views.follow), name='follow'),
    url(r'^user_profile/(?P<pk>\d+)/unfollow/$', login_required(views.unfollow), name='unfollow'),
)

urlpatterns += patterns('', url(r'^rest/', include(router.urls)))
