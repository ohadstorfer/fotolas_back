# Generated by Django 4.2.8 on 2024-11-09 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0055_alter_albumsprices_price_1_to_5_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='stripe_account_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='verification_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
