# Generated by Django 4.2.7 on 2023-11-22 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]