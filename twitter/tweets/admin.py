from django.contrib import admin
from tweets import models
from dbparti import admin as pt_admin


class TweetAdmin(pt_admin.PartitionableAdmin):
    partition_show = 'all'

# Register your models here.
admin.site.register(models.TwitterUser)
admin.site.register(models.Tweet, TweetAdmin)
admin.site.register(models.Following)
