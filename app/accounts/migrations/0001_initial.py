# Generated by Django 2.2.6 on 2021-12-10 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=100, unique=True)),
                ('name', models.CharField(max_length=40, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('tin_no', models.CharField(max_length=40, unique=True)),
                ('gst_no', models.CharField(max_length=40, unique=True)),
                ('pan_no', models.CharField(max_length=40, unique=True)),
                ('other_no', models.CharField(max_length=40)),
                ('contact_phone', models.IntegerField()),
                ('contact_mobile', models.IntegerField()),
                ('address', models.CharField(max_length=40)),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_at', models.DateTimeField(auto_now_add=True, verbose_name='modified date')),
                ('created_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
                'db_table': 'accounts_info',
            },
        ),
        migrations.CreateModel(
            name='LoanAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=100, unique=True)),
                ('owners_name', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=50)),
                ('bank_name', models.CharField(blank=True, max_length=50)),
                ('phone_number', models.CharField(max_length=12)),
                ('notes', models.TextField(blank=True, max_length=400, null=True)),
                ('address', models.TextField(blank=True, max_length=400, null=True)),
                ('status', models.BooleanField(default=False, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_at', models.DateTimeField(auto_now_add=True, verbose_name='modified date')),
            ],
            options={
                'verbose_name_plural': 'Loan Accounts',
                'db_table': 'accounts_loan_accounts',
            },
        ),
        migrations.CreateModel(
            name='MasterExpenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=100, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('notes', models.TextField(blank=True, max_length=400, null=True)),
                ('status', models.BooleanField(default=False, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_at', models.DateTimeField(auto_now_add=True, verbose_name='modified date')),
            ],
            options={
                'verbose_name_plural': 'Master Expenses',
                'db_table': 'accounts_master_expenses',
            },
        ),
        migrations.CreateModel(
            name='PaymentTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=100, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(default=False, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_at', models.DateTimeField(auto_now_add=True, verbose_name='modified date')),
            ],
            options={
                'verbose_name_plural': 'Payment Types',
                'db_table': 'accounts_payment_types',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=100, unique=True)),
                ('id_proof', models.CharField(max_length=30, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=12)),
                ('alternative_phone', models.CharField(blank=True, max_length=12)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, default='default-avatar.png', null=True, upload_to='profile/')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('address', models.TextField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_at', models.DateTimeField(auto_now_add=True, verbose_name='modified date')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='accounts.Accounts')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='auth.Group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'Profiles',
                'db_table': 'accounts_profile',
            },
        ),
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(max_length=30, unique=True)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('state', models.CharField(blank=True, max_length=50)),
                ('pincode', models.PositiveIntegerField()),
                ('country', models.CharField(blank=True, max_length=50)),
                ('address', models.TextField(blank=True, max_length=2000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('modified_at', models.DateTimeField(auto_now_add=True, verbose_name='modified date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Customer Address',
                'db_table': 'accounts_customer_address',
            },
        ),
    ]
