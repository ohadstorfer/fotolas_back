# Generated by Django 4.2.8 on 2024-05-15 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_file_alter_img_personal_album_wave_img_wave'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='img',
            name='personal_album',
        ),
        migrations.AlterField(
            model_name='img',
            name='wave',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='base.wave'),
        ),
    ]
