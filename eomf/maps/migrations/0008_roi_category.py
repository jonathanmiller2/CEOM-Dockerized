# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '__first__'),
        ('maps', '0007_auto_20151205_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='roi',
            name='category',
            field=models.ForeignKey(related_name='rois', db_column=b'categoryid', blank=True, to='photos.Category', null=True),
        ),
    ]
