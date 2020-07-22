# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maps', '0005_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='poi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('score', models.IntegerField(null=True, blank=True)),
                ('Attribute', models.TextField(verbose_name=b'Attributes')),
                ('classification', models.CharField(max_length=500, null=True, verbose_name=b'Site Category', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name=b'modified')),
                ('user', models.ForeignKey(default=1829, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
