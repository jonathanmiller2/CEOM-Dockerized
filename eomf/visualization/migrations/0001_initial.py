# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import eomf.visualization.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_dataset_is_global'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleTimeSeriesJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.CharField(max_length=50, null=True, blank=True)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('row', models.IntegerField(null=True, blank=True)),
                ('col', models.IntegerField(null=True, blank=True)),
                ('tile', models.CharField(max_length=6, null=True, blank=True)),
                ('result', models.FileField(max_length=300, null=True, upload_to=b'visualization/timeseries/single', blank=True)),
                ('years', models.CommaSeparatedIntegerField(max_length=150, verbose_name=b'Select years')),
                ('completed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name=b'modified')),
                ('product', models.ForeignKey(to='inventory.Dataset')),
                ('user', models.ForeignKey(default=1096, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSeriesJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender', models.EmailField(max_length=150, null=True, verbose_name=b'Additional sender', blank=True)),
                ('points', models.FileField(upload_to=b'visualization/timeseries/input', max_length=300, verbose_name=b'Upload csv file', validators=[eomf.visualization.models.checkFormat])),
                ('result', models.FileField(max_length=300, null=True, upload_to=b'visualization/timeseries/multi', blank=True)),
                ('years', models.CommaSeparatedIntegerField(max_length=150, verbose_name=b'Select years')),
                ('completed', models.BooleanField(default=False)),
                ('working', models.BooleanField(default=False)),
                ('error', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('message', models.CharField(max_length=150, null=True, blank=True)),
                ('task_id', models.CharField(max_length=50, null=True, blank=True)),
                ('total_sites', models.IntegerField(default=1)),
                ('progress', models.IntegerField(default=0)),
                ('product', models.ForeignKey(to='inventory.Dataset')),
                ('user', models.ForeignKey(default=1096, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
