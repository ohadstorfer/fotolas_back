# Generated by Django 4.2.8 on 2023-12-21 19:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_photographer_cover_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalalbum',
            name='photographer',
        ),
        migrations.AddField(
            model_name='personalalbum',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
