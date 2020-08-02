# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '__first__'),
        ('maps', '0008_roi_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='poi',
            name='category',
            field=models.ForeignKey(related_name='pois', db_column=b'categoryid', blank=True, to='photos.Category', null=True),
        ),
    ]
