# Generated by Django 3.1.3 on 2020-11-26 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story_auth', '0003_writer_approved'),
        ('story_app', '0019_auto_20201125_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='favorites',
            field=models.ManyToManyField(blank=True, db_table='Favorites', related_name='favorites', to='story_auth.UserProfile'),
        ),
    ]
