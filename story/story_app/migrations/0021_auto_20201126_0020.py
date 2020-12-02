# Generated by Django 3.1.3 on 2020-11-26 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story_auth', '0003_writer_approved'),
        ('story_app', '0020_auto_20201126_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorites', to='story_auth.UserProfile'),
        ),
    ]