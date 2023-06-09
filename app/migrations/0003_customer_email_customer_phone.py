# Generated by Django 4.0.5 on 2022-07-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_quality_cart_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=70, unique=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]
