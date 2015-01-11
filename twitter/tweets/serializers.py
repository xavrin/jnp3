from django.contrib.auth import models as auth_models

from rest_framework import serializers

from tweets.models import Tweet, TwitterUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.User
        fields = ('username', 'first_name', 'last_name',)


class TwitterUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TwitterUser
        fields = ('user',)


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('author', 'created', 'content')