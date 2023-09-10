# Generated by Django 2.2.6 on 2021-12-24 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20211224_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='gst',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='igst',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='purchase_type',
            field=models.CharField(blank=True, choices=[('WITH_TAX', 'With Tax'), ('WITHOUT_TAX', 'Without Tax')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='tax_type',
            field=models.CharField(blank=True, choices=[('GST', 'GST'), ('IGST', 'IGST')], max_length=50, null=True),
        ),
    ]
