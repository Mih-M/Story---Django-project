# Generated by Django 3.1.3 on 2020-11-24 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story_app', '0013_story_writer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='category',
            field=models.CharField(choices=[('FN', 'fun'), ('LV', 'love'), ('UE', 'unexpected-end'), ('MY', 'mystery'), ('FT', 'fairy-tail'), ('FA', 'fantasy')], max_length=20),
        ),
    ]
