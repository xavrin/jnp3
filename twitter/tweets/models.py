from django.contrib.auth import models as auth_models
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from dbparti import models as pt_models
from djorm_pgfulltext.fields import VectorField
from djorm_pgfulltext.models import SearchManager


class TwitterUser(models.Model):
    user = models.ForeignKey(auth_models.User)
    # also avatar

    def __unicode__(self):
        return unicode(self.user)


class Following(models.Model):
    follower = models.ForeignKey(TwitterUser, related_name='followers')
    followee = models.ForeignKey(TwitterUser, related_name='folowees')

    def __unicode__(self):
        return "{}->{}".format(unicode(self.follower), unicode(self.followee))


class Tweet(pt_models.Partitionable):
    author = models.ForeignKey(TwitterUser)
    created = models.DateTimeField('date of publication')
    content = models.CharField(max_length=140)

    search_index = VectorField()

    objects = SearchManager(
        fields=('content',),
        config='pg_catalog.english',  # this is default
        search_field='search_index',  # this is default
        auto_update_search_field=True
    )

    class Meta(pt_models.Partitionable.Meta):
        partition_type = 'range'
        partition_subtype = 'date'
        partition_range = 'day'
        partition_column = 'created'

    def __unicode__(self):
        return self.content[:20]


@receiver(post_save, sender=auth_models.User)
def init_new_user(sender, instance, signal, created, **kwargs):
    if created:
        TwitterUser.objects.create(user=instance)