# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='phenocam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sitename', models.CharField(max_length=50, blank=True)),
                ('takendate', models.DateTimeField(null=True, blank=True)),
                ('red', models.DecimalField(null=True, max_digits=20, decimal_places=18, blank=True)),
                ('green', models.DecimalField(null=True, max_digits=20, decimal_places=18, blank=True)),
                ('blue', models.DecimalField(null=True, max_digits=20, decimal_places=18, blank=True)),
                ('gcc', models.DecimalField(null=True, max_digits=20, decimal_places=18, blank=True)),
            ],
        ),
    ]
