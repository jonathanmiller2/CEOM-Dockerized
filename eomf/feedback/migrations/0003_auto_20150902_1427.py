# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20150902_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='Photo',
            field=models.ImageField(default=b'media/feedback/image5.jpg', null=True, upload_to=b'media/feedback', blank=True),
        ),
    ]
