# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_auto_20150717_0537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapoint',
            name='datum',
            field=models.CharField(max_length=140),
        ),
    ]
