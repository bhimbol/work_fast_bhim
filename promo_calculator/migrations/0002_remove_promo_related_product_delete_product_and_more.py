# Generated by Django 4.0.6 on 2024-02-24 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promo_calculator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promo',
            name='related_product',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Promo',
        ),
    ]