# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0002_auto_20150715_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='reviewers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='data_point_reviewers'),
        ),
        migrations.AddField(
            model_name='note',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='reviewers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='note_reviewers'),
        ),
        migrations.AddField(
            model_name='searchquery',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
