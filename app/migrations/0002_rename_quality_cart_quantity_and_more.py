# Generated by Django 4.0.5 on 2022-07-04 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='quality',
            new_name='quantity',
        ),
        migrations.RenameField(
            model_name='orderplaced',
            old_name='ondered_data',
            new_name='ordered_date',
        ),
        migrations.RenameField(
            model_name='orderplaced',
            old_name='quantiy',
            new_name='quantity',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='descriptionn',
            new_name='description',
        ),
    ]