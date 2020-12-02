# Generated by Django 3.1.3 on 2020-11-25 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story_auth', '0003_writer_approved'),
        ('story_app', '0018_auto_20201125_2327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='like',
            new_name='likes',
        ),
        migrations.RemoveField(
            model_name='story',
            name='favorite',
        ),
        migrations.AddField(
            model_name='story',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorites', to='story_auth.UserProfile'),
        ),
    ]