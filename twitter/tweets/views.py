from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template.context import RequestContext
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
import json

from rest_framework import viewsets
from registration.backends.simple.views import RegistrationView
import datetime
from tweets.models import Tweet, TwitterUser, Following

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
        followee = TwitterUser.objects.get(pk=self.profile_pk)
        follower = TwitterUser.objects.get(user=self.request.user.pk)
        context['following'] = Following.objects.filter(follower=follower.pk, followee=followee.pk).count() > 0
        return context


class HomeView(ListView):
    context_object_name = 'tweets'
    template_name = 'home.html'
    paginate_by = 4
    model = Tweet

    def get_queryset(self):
        if self.request.user.is_authenticated():
            user = self.request.user.twitteruser
            followees = Following.objects.filter(follower=user).values('followee')
            return Tweet.objects.filter(author__in=followees).order_by('-created')
        else:
            return Tweet.objects.none()

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['no_tweets_message'] = "There are no new tweets."
        return context


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


def follow(request, pk):
    result = {"success": False}

    if request.POST:
        if request.POST.get('user_to_follow'):
            followee = (TwitterUser.objects.get(pk=int(json.loads(request.POST.get('user_to_follow')))))
            follower = TwitterUser.objects.get(user=request.user.pk)
            if (follower is not None and followee is not None and
               Following.objects.filter(follower=follower.pk, followee=followee.pk).count() == 0):
                new_following = Following(follower=follower, followee=followee)
                new_following.save()
                result["success"] = True

    result = json.dumps(result)
    return HttpResponse(result, 'aplication/json')


def unfollow(request, pk):
    result = {"success": False}

    if request.POST:
        if request.POST.get('user_to_follow'):
            followee = (TwitterUser.objects.get(pk=int(json.loads(request.POST.get('user_to_follow')))))
            follower = TwitterUser.objects.get(user=request.user.pk)
            if (follower is not None and followee is not None and
               Following.objects.filter(follower=follower.pk, followee=followee.pk).count() == 1):
                new_following = Following.objects.get(follower=follower.pk, followee=followee.pk)
                new_following.delete()
                result["success"] = True

    result = json.dumps(result)
    return HttpResponse(result, 'aplication/json')


class TweetSearchView(ListView):
    context_object_name = 'tweets'
    template_name = 'tweets.html'
    paginate_by = 4
    model = Tweet

    def get_queryset(self):
        search_query = ""
        if self.request.GET:
            search_query = self.request.GET.get('search_query')
        return Tweet.objects.search(search_query)

    def get_context_data(self, *args, **kwargs):
        context = super(TweetSearchView, self).get_context_data(*args, **kwargs)
        context['no_tweets_message'] = "There are no results satisfying the given query :("
        return context
