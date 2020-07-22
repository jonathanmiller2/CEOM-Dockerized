# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0004_map_gallery_map_image_legend'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_comment', models.CharField(max_length=3000, verbose_name=b'Your Name')),
                ('Comment_text', models.TextField(verbose_name=b'Enter Comment here')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'created')),
                ('Comment_id', models.ForeignKey(related_name='comment', to='maps.map_gallery')),
            ],
        ),
    ]
