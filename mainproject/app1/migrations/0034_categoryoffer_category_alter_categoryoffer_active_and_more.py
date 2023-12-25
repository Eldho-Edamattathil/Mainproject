# Generated by Django 4.2.7 on 2023-12-23 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0033_categoryoffer_productoffer'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryoffer',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.category'),
        ),
        migrations.AlterField(
            model_name='categoryoffer',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='productoffer',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
