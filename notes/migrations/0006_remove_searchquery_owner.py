# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_auto_20150717_0542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchquery',
            name='owner',
        ),
    ]
