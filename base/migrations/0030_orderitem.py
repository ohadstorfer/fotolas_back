# Generated by Django 4.2.8 on 2024-05-23 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_albumsprices'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Wave', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.wave')),
                ('img_quantity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.img')),
                ('orderId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='base.order')),
            ],
        ),
    ]
