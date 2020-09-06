# Generated by Django 2.2.13 on 2020-08-05 20:18

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import eomf.photos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.IntegerField()),
                ('id_prim', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=40)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='ContinentBuffered',
            fields=[
                ('gid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='continent', max_length=13)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
            ],
            options={
                'verbose_name': 'Continent',
                'verbose_name_plural': 'Continents',
                'db_table': 'continent_buffered',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('gid', models.IntegerField(primary_key=True, serialize=False)),
                ('fips_cntry', models.CharField(blank=True, max_length=2)),
                ('gmi_cntry', models.CharField(blank=True, max_length=3)),
                ('iso_2digit', models.CharField(blank=True, max_length=2)),
                ('iso_3digit', models.CharField(blank=True, max_length=3)),
                ('iso_num', models.IntegerField(blank=True, null=True)),
                ('cntry_name', models.CharField(blank=True, max_length=40)),
                ('long_name', models.CharField(blank=True, max_length=40)),
                ('isoshrtnam', models.CharField(blank=True, max_length=45)),
                ('unshrtnam', models.CharField(blank=True, max_length=55)),
                ('locshrtnam', models.CharField(blank=True, max_length=43)),
                ('loclngnam', models.CharField(blank=True, max_length=74)),
                ('status', models.CharField(blank=True, max_length=60)),
                ('pop2007', models.BigIntegerField(blank=True, null=True)),
                ('sqkm', models.FloatField(blank=True, null=True)),
                ('sqmi', models.FloatField(blank=True, null=True)),
                ('land_sqkm', models.IntegerField(blank=True, null=True)),
                ('colormap', models.IntegerField(blank=True, null=True)),
                ('_oid', models.IntegerField(blank=True, null=True)),
                ('the_geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='CountryBuffered',
            fields=[
                ('gid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='cntry_name', max_length=40)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'db_table': 'country_buffered',
            },
        ),
        migrations.CreateModel(
            name='PhotoUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=30)),
                ('password', models.CharField(blank=True, max_length=32)),
                ('infoid', models.IntegerField(blank=True, null=True)),
                ('roleid', models.IntegerField(blank=True, null=True)),
                ('createdate', models.DateTimeField(blank=True, null=True)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('researchid', models.IntegerField(blank=True, null=True)),
                ('timestamp', models.IntegerField(blank=True, null=True)),
                ('sessid', models.CharField(blank=True, max_length=32)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('affiliation', models.CharField(blank=True, max_length=250)),
                ('telephone', models.CharField(blank=True, max_length=20)),
                ('address1', models.CharField(blank=True, max_length=50)),
                ('address2', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('state', models.CharField(blank=True, max_length=80)),
                ('postal', models.CharField(blank=True, max_length=10)),
                ('country', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name': 'Photo User',
                'verbose_name_plural': 'Photo Users',
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('gid', models.IntegerField(primary_key=True, serialize=False)),
                ('region', models.CharField(blank=True, max_length=21)),
                ('sqmi', models.DecimalField(blank=True, decimal_places=999, max_digits=999, null=True)),
                ('sqkm', models.DecimalField(blank=True, decimal_places=999, max_digits=999, null=True)),
                ('_oid', models.IntegerField(blank=True, null=True)),
                ('the_geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
                'db_table': 'region',
            },
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=16)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Research',
                'verbose_name_plural': 'Researches',
                'db_table': 'research',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('icon', models.ImageField(upload_to='photos/themes/')),
            ],
            options={
                'verbose_name': 'Theme',
                'verbose_name_plural': 'Themes',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(blank=True, db_column='location', max_length=300, storage=django.core.files.storage.FileSystemStorage(base_url='/media/photos/', location='/code/eomf/media/photos'), upload_to=eomf.photos.models.photo_path)),
                ('notes', models.TextField(blank=True, db_column='description')),
                ('_lon', models.FloatField(blank=True, db_column='long', null=True)),
                ('_lat', models.FloatField(blank=True, db_column='lat', null=True)),
                ('regionid', models.IntegerField(blank=True, null=True)),
                ('takendate', models.DateField(blank=True, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('uploaddate', models.DateField(auto_now_add=True, null=True)),
                ('datum', models.CharField(blank=True, max_length=8)),
                ('alt', models.FloatField(blank=True, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('dir_card', models.CharField(blank=True, choices=[('N', 'North'), ('NNE', 'NNE'), ('NE', 'NE'), ('ENE', 'ENE'), ('E', 'East'), ('ESE', 'ESE'), ('SE', 'SE'), ('SSE', 'SSE'), ('S', 'South'), ('SSW', 'SSW'), ('SW', 'SW'), ('WSW', 'WSW'), ('W', 'West'), ('WNW', 'WNW'), ('NW', 'NW'), ('NNW', 'NNW')], db_column='dir', max_length=4)),
                ('dir_deg', models.FloatField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Deleted'), (1, 'Public'), (2, 'Private')], default=1, null=True)),
                ('file_hash', models.CharField(blank=True, db_column='hash', max_length=32)),
                ('source', models.CharField(blank=True, max_length=100)),
                ('category', models.ForeignKey(blank=True, db_column='categoryid', null=True, on_delete=django.db.models.deletion.CASCADE, to='photos.Category')),
                ('theme', models.ForeignKey(blank=True, db_column='photogroupid', null=True, on_delete=django.db.models.deletion.CASCADE, to='photos.Theme')),
                ('user', models.ForeignKey(blank=True, db_column='userid', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
                'db_table': 'photos',
            },
        ),
    ]