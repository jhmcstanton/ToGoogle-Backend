# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_auto_20150718_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='last_analyzed',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 19, 4, 5, 4, 355361, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='note',
            name='last_analyzed',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 19, 4, 5, 17, 785266, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
