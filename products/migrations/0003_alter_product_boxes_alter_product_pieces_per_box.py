# Generated by Django 5.1.3 on 2024-11-11 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='boxes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='pieces_per_box',
            field=models.IntegerField(default=0),
        ),
    ]
