# Generated by Django 4.1.7 on 2023-03-30 17:57

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpbackend', '0006_alter_karta_putpredmet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='putovnipredmet',
            name='karty',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=12), blank=True, default=list, size=None),
        ),
    ]
