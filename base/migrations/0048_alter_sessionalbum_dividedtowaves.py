# Generated by Django 4.2.8 on 2024-08-27 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0047_alter_sessionalbum_dividedtowaves'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionalbum',
            name='dividedToWaves',
            field=models.BooleanField(null=True),
        ),
    ]
