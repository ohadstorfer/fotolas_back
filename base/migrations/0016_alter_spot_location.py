# Generated by Django 4.2.8 on 2024-01-30 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_photographer_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
