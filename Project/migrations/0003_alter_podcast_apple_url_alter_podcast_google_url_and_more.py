# Generated by Django 5.0.4 on 2024-05-01 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0002_remove_podcast_urls_podcast_apple_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcast',
            name='apple_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='google_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='spotify_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='youtube_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]