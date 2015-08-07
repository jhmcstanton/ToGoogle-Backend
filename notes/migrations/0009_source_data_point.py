# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_auto_20150719_0405'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='data_point',
            field=models.OneToOneField(to='notes.DataPoint', default=1),
            preserve_default=False,
        ),
    ]
