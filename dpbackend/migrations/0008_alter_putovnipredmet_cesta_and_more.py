# Generated by Django 4.1.7 on 2023-03-30 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpbackend', '0007_alter_putovnipredmet_karty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='putovnipredmet',
            name='cesta',
            field=models.CharField(default='images/', max_length=100),
        ),
        migrations.AlterField(
            model_name='putovnipredmet',
            name='obrazek',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
