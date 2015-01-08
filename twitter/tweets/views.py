from django.shortcuts import render, render_to_response
from django.template.context import RequestContext

from rest_framework import viewsets

from tweets.models import Tweet, TwitterUser
from tweets.serializers import TweetSerializer, TwitterUserSerializer


def home(request):
    context = RequestContext(request, {'request': request, 'user': request.user})
    return render_to_response('home.html', context_instance=context)


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class TwitterUserViewSet(viewsets.ModelViewSet):
    queryset = TwitterUser.objects.all()
    serializer_class = TwitterUserSerializer