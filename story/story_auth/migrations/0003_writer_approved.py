# Generated by Django 3.1.3 on 2020-11-23 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story_auth', '0002_auto_20201122_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='writer',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]