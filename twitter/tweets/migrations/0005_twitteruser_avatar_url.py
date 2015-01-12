# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_auto_20150111_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='avatar_url',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
