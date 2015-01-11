from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from rest_framework import viewsets
from registration.backends.simple.views import RegistrationView

from tweets.models import Tweet, TwitterUser
from tweets.serializers import TweetSerializer, TwitterUserSerializer


class HomeView(TemplateView):
    template_name='home.html'


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
