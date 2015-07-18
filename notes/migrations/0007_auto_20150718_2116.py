# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_remove_searchquery_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='similar_data_points',
            field=models.ManyToManyField(to='notes.DataPoint', related_name='similar_data_points_rel_+'),
        ),
        migrations.AddField(
            model_name='note',
            name='similar_notes',
            field=models.ManyToManyField(to='notes.Note', related_name='similar_notes_rel_+'),
        ),
    ]
