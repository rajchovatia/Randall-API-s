# Generated by Django 5.0.4 on 2024-05-01 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0004_subscribe'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookRandall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=240, null=True)),
                ('last_name', models.CharField(blank=True, max_length=240, null=True)),
                ('email', models.EmailField(blank=True, max_length=240, null=True)),
                ('subject', models.CharField(blank=True, max_length=240, null=True)),
                ('message', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
