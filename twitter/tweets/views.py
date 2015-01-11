from django.shortcuts import render, render_to_response, redirect
from django.template.context import RequestContext
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework import viewsets
from registration.backends.simple.views import RegistrationView
import datetime
from django.http import HttpResponse
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

def search(request):
    errors = []
    if 'username' in request.GET:
        username = request.GET['username']
        if not username:
            errors.append('Enter a search term.')
        else:
            users = TwitterUser.objects.filter(user__username__icontains = username)
            return render(request, 'search_results.html',
                {'users': users, 'query': username})
    return render(request, 'search.html',
        {'errors': errors})


class TweetDetailView(DetailView):
    template_name = "tweet_detail.html"
    model = Tweet
    context_object_name = "tweet"


class UserTweetsView(ListView):
    context_object_name = 'tweets'
    template_name = 'user_tweets.html'
    paginate_by = 4
    model = Tweet

    def get(self, request, *args, **kwargs):
        self.profile_pk = self.kwargs['pk']
        return super(UserTweetsView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        user = TwitterUser.objects.get(pk=self.profile_pk)
        return Tweet.objects.filter(author=user)

    def get_context_data(self, *args, **kwargs):
        context = super(UserTweetsView, self).get_context_data(*args, **kwargs)
        context['profile'] = TwitterUser.objects.get(pk=self.profile_pk)
        return context


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
