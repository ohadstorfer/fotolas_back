# Generated by Django 4.2.8 on 2023-12-21 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_customuser_country_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photographer',
            name='info',
        ),
    ]
