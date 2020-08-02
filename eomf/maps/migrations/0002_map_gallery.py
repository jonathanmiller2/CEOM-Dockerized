# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='map_gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('map_image', models.ImageField(default=b'media/feedback/image5.jpg', upload_to=b'media/map_gallery')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=3000)),
                ('name_uploader', models.CharField(max_length=3000)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name=b'modified')),
                ('validated', models.BooleanField()),
                ('user', models.ForeignKey(default=1829, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
