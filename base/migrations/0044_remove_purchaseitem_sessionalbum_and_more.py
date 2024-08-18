# Generated by Django 4.2.8 on 2024-08-08 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0043_alter_img_wave_alter_sessionalbum_dividedtowaves'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseitem',
            name='SessionAlbum',
        ),
        migrations.RemoveField(
            model_name='purchaseitem',
            name='item_quantity',
        ),
        migrations.AddField(
            model_name='purchase',
            name='SessionAlbum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.sessionalbum'),
        ),
    ]
