# Generated by Django 2.2.6 on 2021-12-12 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_expenses_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='expense_date',
            field=models.DateTimeField(verbose_name='expense date'),
        ),
    ]
