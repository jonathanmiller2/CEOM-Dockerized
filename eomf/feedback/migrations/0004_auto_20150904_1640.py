# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20150902_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task_status',
            name='feedback_track',
            field=models.OneToOneField(related_name='stats', primary_key=True, serialize=False, to='feedback.Feedback', on_delete=models.CASCADE),
        ),
    ]
