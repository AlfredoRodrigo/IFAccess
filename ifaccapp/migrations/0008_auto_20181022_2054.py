# Generated by Django 2.0.8 on 2018-10-22 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifaccapp', '0007_auto_20180930_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambient',
            name='IP',
            field=models.TextField(max_length=15, null=True, verbose_name='IP'),
        ),
        migrations.AddField(
            model_name='ambient',
            name='mask',
            field=models.TextField(max_length=15, null=True, verbose_name='Máscara'),
        ),
    ]
