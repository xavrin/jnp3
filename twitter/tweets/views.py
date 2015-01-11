from django.shortcuts import render, render_to_response, redirect
from django.template.context import RequestContext
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse

from rest_framework import viewsets
from registration.backends.simple.views import RegistrationView
import datetime

from tweets.models import Tweet, TwitterUser
from tweets.serializers import TweetSerializer, TwitterUserSerializer


class TweetCreateView(CreateView):
    template_name = "create_tweet.html"
    model = Tweet
    fields = ['content']

    def form_valid(self, form):
        tweet = form.save(commit=False)
        tweet.created = datetime.datetime.now()
        tweet.author = self.request.user.twitteruser
        tweet.save()
        return redirect('show_tweet', pk=tweet.pk)


class TweetDetailView(DetailView):
    template_name = "tweet_detail.html"
    model = Tweet
    context_object_name = "tweet"


class HomeView(TemplateView):
    template_name = 'home.html'


class RegistrationURLView(RegistrationView):
    template_name = "registration_form.html"

    def get_success_url(self, *args, **kwargs):
        return reverse('home')


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class TwitterUserViewSet(viewsets.ModelViewSet):
    queryset = TwitterUser.objects.all()
    serializer_class = TwitterUserSerializer
