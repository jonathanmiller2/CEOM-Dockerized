# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0002_map_gallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map_gallery',
            name='description',
            field=models.TextField(verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='map_gallery',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name=b'Email'),
        ),
        migrations.AlterField(
            model_name='map_gallery',
            name='map_image',
            field=models.ImageField(default=b'media/feedback/image5.jpg', upload_to=b'media/map_gallery', verbose_name=b'Upload Map'),
        ),
        migrations.AlterField(
            model_name='map_gallery',
            name='name_uploader',
            field=models.CharField(max_length=3000, verbose_name=b'Your Name'),
        ),
        migrations.AlterField(
            model_name='map_gallery',
            name='title',
            field=models.CharField(max_length=3000, verbose_name=b'Title of your map'),
        ),
    ]
