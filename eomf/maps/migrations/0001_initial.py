# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='roi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('tile', models.CharField(max_length=6, null=True, blank=True)),
                ('image', models.ImageField(default=b'media/feedback/image5.jpg', null=True, upload_to=b'media/roi', blank=True)),
                ('score', models.IntegerField(null=True, blank=True)),
                ('description', models.TextField()),
                ('classification', models.CharField(max_length=255, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name=b'modified')),
                ('pixelsize', models.IntegerField()),
                ('user', models.ForeignKey(default=1096, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
