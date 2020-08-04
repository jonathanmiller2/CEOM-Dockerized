# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_auto_20150904_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='Comment_id',
            field=models.ForeignKey(related_name='comment', to='feedback.Feedback', on_delete=models.CASCADE),
        ),
    ]
