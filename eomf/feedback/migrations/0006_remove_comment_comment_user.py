# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_auto_20150904_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='Comment_user',
        ),
    ]
