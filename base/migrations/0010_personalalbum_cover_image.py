# Generated by Django 4.2.8 on 2023-12-31 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_remove_order_personal_album_img_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalalbum',
            name='cover_image',
            field=models.ImageField(default='default.png', upload_to=''),
        ),
    ]
