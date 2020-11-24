# Generated by Django 3.1.3 on 2020-11-03 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='content',
            field=models.TextField(default='lorem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='story',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
