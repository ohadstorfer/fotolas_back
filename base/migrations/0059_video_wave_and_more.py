# Generated by Django 4.2.8 on 2024-11-29 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0058_alter_defaultalbumspricesforimages_price_1_to_5_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='wave',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.wave'),
        ),
        migrations.AlterField(
            model_name='defaultalbumspricesforvideos',
            name='price_16_plus',
            field=models.DecimalField(decimal_places=1, default=30.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='defaultalbumspricesforvideos',
            name='price_1_to_3',
            field=models.DecimalField(decimal_places=1, default=20.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='defaultalbumspricesforvideos',
            name='price_4_to_15',
            field=models.DecimalField(decimal_places=1, default=25.0, max_digits=10),
        ),
    ]