# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('datum', models.CharField(max_length=50)),
                ('creation_date_time', models.DateTimeField(auto_now_add=True)),
                ('last_edit_date_time', models.DateTimeField(auto_now=True)),
                ('is_factual', models.BooleanField()),
                ('private', models.BooleanField()),
            ],
            options={
                'ordering': ('last_edit_date_time', 'creation_date_time'),
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('summary', models.TextField(max_length=255)),
                ('creation_date_time', models.DateTimeField(auto_now_add=True)),
                ('last_edit_date_time', models.DateTimeField(auto_now=True)),
                ('private', models.BooleanField()),
            ],
            options={
                'ordering': ('last_edit_date_time', 'creation_date_time'),
            },
        ),
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('query', models.CharField(max_length=255)),
                ('date_time_queried', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(to='notes.Note')),
            ],
            options={
                'ordering': ('date_time_queried',),
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('url', models.CharField(max_length=255)),
                ('found_date', models.DateTimeField(auto_now_add=True)),
                ('last_edit_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('tag', models.CharField(max_length=16)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('data_points', models.ForeignKey(to='notes.DataPoint')),
                ('notes', models.ForeignKey(to='notes.Note')),
                ('sources', models.ForeignKey(to='notes.Source')),
            ],
        ),
        migrations.AddField(
            model_name='datapoint',
            name='notes',
            field=models.ManyToManyField(to='notes.Note'),
        ),
    ]
