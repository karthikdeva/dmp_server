# Generated by Django 2.2.6 on 2023-09-10 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataStore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='citizen',
            name='noOneAtHome',
            field=models.BooleanField(default=False, verbose_name='notavailable'),
        ),
    ]
