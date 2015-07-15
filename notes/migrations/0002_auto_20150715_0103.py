# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapoint',
            name='notes',
            field=models.ManyToManyField(to='notes.Note', related_query_name='data_point', related_name='data_points'),
        ),
        migrations.RemoveField(
            model_name='tag',
            name='data_points',
        ),
        migrations.AddField(
            model_name='tag',
            name='data_points',
            field=models.ManyToManyField(to='notes.DataPoint'),
        ),
        migrations.RemoveField(
            model_name='tag',
            name='notes',
        ),
        migrations.AddField(
            model_name='tag',
            name='notes',
            field=models.ManyToManyField(to='notes.Note'),
        ),
        migrations.RemoveField(
            model_name='tag',
            name='sources',
        ),
        migrations.AddField(
            model_name='tag',
            name='sources',
            field=models.ManyToManyField(to='notes.Source'),
        ),
    ]
