# Generated by Django 3.1.3 on 2020-12-03 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('story_auth', '0004_auto_20201127_1647'),
        ('story_app', '0021_auto_20201126_0020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=20)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='story_app.story')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='story_auth.userprofile')),
            ],
        ),
        migrations.RemoveField(
            model_name='story',
            name='likes',
        ),

        migrations.AddField(
            model_name='story',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', through='story_app.Like',
                                         to='story_auth.UserProfile'),
        ),
    ]
