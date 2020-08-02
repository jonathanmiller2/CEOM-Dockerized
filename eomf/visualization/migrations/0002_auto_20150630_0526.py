# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeseriesjob',
            name='years',
            field=models.CommaSeparatedIntegerField(max_length=75, verbose_name=b'Select years'),
        ),
    ]
