# Generated by Django 2.2.6 on 2021-12-12 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=100, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('hsn_code', models.CharField(max_length=50, null=True)),
                ('price', models.CharField(max_length=50, null=True)),
                ('current_stock', models.CharField(max_length=50, null=True)),
                ('tax', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_at', models.DateTimeField(auto_now_add=True, verbose_name='modified date')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='accounts.Category')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UnitOfMeasurement', to='accounts.UnitOfMeasurement')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'db_table': 'accounts_products',
            },
        ),
    ]
