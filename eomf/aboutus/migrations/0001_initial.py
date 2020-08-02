# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import eomf.aboutus.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', eomf.aboutus.models.YearField(max_length=4)),
                ('order', models.IntegerField()),
                ('title', models.CharField(max_length=100, verbose_name=b'Title')),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('picture', models.ImageField(upload_to=b'aboutus/group_photos/photos')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=125)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100, null=True, blank=True)),
                ('middle_name', models.CharField(max_length=50, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100, null=True, blank=True)),
                ('title', models.CharField(max_length=250, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone', models.CharField(max_length=16, null=True, blank=True)),
                ('link', models.CharField(max_length=250, null=True, blank=True)),
                ('date', models.DateField(null=True, verbose_name=b'date published')),
                ('extra', models.TextField(null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('headshot', models.ImageField(default=b'/media/people/dummy_headshot222.jpg', null=True, upload_to=b'people/')),
                ('order', models.IntegerField(default=9999)),
                ('alumni_group', models.ForeignKey(related_name='personAsAlumniGroup', blank=True, to='aboutus.Group', null=True)),
                ('group', models.ForeignKey(related_name='personAsGroup', to='aboutus.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(verbose_name=b'Post Title')),
                ('date', models.DateField(verbose_name=b'date')),
                ('content', models.TextField(verbose_name=b'Content')),
                ('image_comlumn_number', models.CharField(default=b'1', max_length=1, verbose_name=b' column images', choices=[(b'1', b'One column image'), (b'2', b'Two columns image')])),
            ],
        ),
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=80, verbose_name=b'File title')),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('file_attached', models.FileField(upload_to=b'news/docs')),
                ('post', models.ForeignKey(related_name='files', to='aboutus.Post')),
            ],
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100, verbose_name=b'Description')),
                ('order', models.PositiveIntegerField()),
                ('image', models.ImageField(null=True, upload_to=b'news')),
                ('post', models.ForeignKey(related_name='images', to='aboutus.Post')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='galleryphoto',
            unique_together=set([('year', 'order')]),
        ),
        migrations.AlterUniqueTogether(
            name='postimage',
            unique_together=set([('post', 'order')]),
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('first_name', 'middle_name', 'last_name')]),
        ),
    ]
