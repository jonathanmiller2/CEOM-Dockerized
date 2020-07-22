# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Comment_text', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('text', models.TextField()),
                ('Photo', models.ImageField(upload_to=b'media/feedback')),
                ('Priority', models.CharField(default=b'BNU', max_length=3, choices=[(b'BU', b'Bug_urgent'), (b'BNU', b'Bug_not_urgent'), (b'FT', b'New feature'), (b'UX', b'UX_urgent')])),
                ('feedback_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task_status',
            fields=[
                ('feedback_track', models.OneToOneField(primary_key=True, serialize=False, to='feedback.Feedback')),
                ('assigned_to', models.CharField(default=b'XJ', max_length=2, choices=[(b'BR', b'Bhargav Bolla'), (b'XJ', b'Xibei Jia')])),
                ('task_status', models.CharField(default=b'NW', max_length=2, choices=[(b'CO', b'done'), (b'WR', b'working'), (b'NM', b'need more info'), (b'NW', b'New')])),
            ],
        ),
        migrations.AddField(
            model_name='feedback',
            name='site',
            field=models.ForeignKey(to='sites.Site'),
        ),
        migrations.AddField(
            model_name='comment',
            name='Comment_id',
            field=models.ForeignKey(to='feedback.Feedback'),
        ),
        migrations.AddField(
            model_name='comment',
            name='Comment_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
