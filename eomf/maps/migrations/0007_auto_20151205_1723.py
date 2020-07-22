# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0006_poi'),
    ]

    operations = [
        migrations.AddField(
            model_name='roi',
            name='col',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='roi',
            name='points',
            field=models.TextField(default='none'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roi',
            name='row',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
