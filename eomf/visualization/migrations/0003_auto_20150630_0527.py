# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualization', '0002_auto_20150630_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeseriesjob',
            name='years',
            field=models.CommaSeparatedIntegerField(max_length=150, verbose_name=b'Select years'),
        ),
    ]
