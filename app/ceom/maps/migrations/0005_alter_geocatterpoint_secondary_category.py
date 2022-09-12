# Generated by Django 3.2.15 on 2022-09-11 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0012_REGISTER_ORIGINAL_VOTES'),
        ('maps', '0004_auto_20220911_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geocatterpoint',
            name='secondary_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondary_category', to='photos.category'),
        ),
    ]
