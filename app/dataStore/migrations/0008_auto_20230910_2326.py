# Generated by Django 2.2.6 on 2023-09-10 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataStore', '0007_auto_20230910_2312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citizen',
            old_name='created_time',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='citizen',
            old_name='modified_time',
            new_name='modified_at',
        ),
    ]
