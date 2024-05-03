# Generated by Django 5.0.4 on 2024-05-02 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0007_videos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='testimonial_image/')),
                ('name', models.CharField(blank=True, max_length=240, null=True)),
                ('date', models.CharField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
