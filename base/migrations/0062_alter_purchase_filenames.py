# Generated by Django 4.2.8 on 2024-12-16 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0061_purchase_filenames_purchase_type_purchase_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='filenames',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
