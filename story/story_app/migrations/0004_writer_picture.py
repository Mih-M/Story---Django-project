# Generated by Django 3.1.3 on 2020-11-15 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story_app', '0003_story_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='writer',
            name='picture',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
