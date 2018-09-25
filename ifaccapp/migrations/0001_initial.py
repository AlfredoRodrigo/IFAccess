# Generated by Django 2.0.8 on 2018-09-25 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ambient',
            fields=[
                ('ID', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('registration', models.BigIntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ambient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ifaccapp.Ambient')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ifaccapp.Person')),
            ],
        ),
    ]
