# Generated by Django 5.1.3 on 2024-11-07 09:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_cart_cartitem'),
        ('products', '0005_remove_notification_product'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='status',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='cart',
            name='boxes',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
