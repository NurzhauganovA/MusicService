# Generated by Django 4.0.2 on 2022-04-30 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='text_of_song',
            field=models.TextField(blank=True, null=True, verbose_name='Text of song'),
        ),
    ]
