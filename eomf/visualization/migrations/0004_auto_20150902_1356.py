# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import eomf.visualization.models


class Migration(migrations.Migration):

    dependencies = [
        ('visualization', '0003_auto_20150630_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeseriesjob',
            name='points',
            field=models.FileField(upload_to=b'visualization/timeseries/input', max_length=150, verbose_name=b'Upload csv file', validators=[eomf.visualization.models.checkFormat]),
        ),
        migrations.AlterField(
            model_name='timeseriesjob',
            name='years',
            field=models.CommaSeparatedIntegerField(max_length=200, verbose_name=b'Select years'),
        ),
    ]
