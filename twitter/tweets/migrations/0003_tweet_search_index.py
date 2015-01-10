# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgfulltext.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_auto_20150104_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='search_index',
            field=djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True),
            preserve_default=True,
        ),
    ]
