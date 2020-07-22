# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0003_auto_20151127_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='map_gallery',
            name='map_image_legend',
            field=models.ImageField(default=b'media/feedback/image5.jpg', upload_to=b'media/map_gallery', verbose_name=b'Legend'),
        ),
    ]
