# Generated by Django 4.2.7 on 2023-11-26 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0018_remove_varients_image_product_varient_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Varients',
            new_name='Variants',
        ),
    ]
