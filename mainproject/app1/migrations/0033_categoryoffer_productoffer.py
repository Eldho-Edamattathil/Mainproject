# Generated by Django 4.2.7 on 2023-12-23 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0032_cartorder_wallet_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
