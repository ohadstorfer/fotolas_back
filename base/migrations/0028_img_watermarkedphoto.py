# Generated by Django 4.2.8 on 2024-05-17 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_remove_censoredimg_img_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='img',
            name='WatermarkedPhoto',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
