# Generated by Django 5.1.3 on 2024-11-06 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('manufactured_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('boxes', models.IntegerField()),
                ('pieces_per_box', models.IntegerField()),
                ('pieces_left', models.IntegerField()),
                ('boxes_left', models.IntegerField(default=0)),
                ('section', models.CharField(blank=True, max_length=255, null=True)),
                ('store_name', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
