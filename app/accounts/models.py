from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, logout, get_user_model, user_logged_in, user_logged_out
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import uuid
import os

from django.db import models
from django.utils.html import mark_safe
from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html
# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from rest_framework import fields
from django.core.mail import send_mail  
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from app.accounts.static import TABLE_PREFIX

class Citizen(models.Model):
    PREFIX = 'CIT'

    # Custom model field for the unique citizen ID with a prefix
    citizen_id = models.CharField(max_length=20, unique=True, db_index=True)

    name = models.CharField(max_length=255, validators=[validators.MinLengthValidator(limit_value=25, message='Name must be at least 25 characters long.')])
    mobile1 = models.CharField(max_length=10, validators=[validators.RegexValidator(r'^\d{10}$', message='Mobile number must be exactly 10 digits.')])
    mobile2 = models.CharField(max_length=10, validators=[validators.RegexValidator(r'^\d{10}$', message='Mobile number must be exactly 10 digits.')])
    doorNumber = models.CharField(max_length=50)
    nameOnNamePlate = models.CharField(max_length=255)
    adharNumber = models.CharField(max_length=12, validators=[validators.RegexValidator(r'^\d{12}$', message='Adhar number must be 12 digits.')])
    geoLocation = models.CharField(max_length=255, blank=True, null=True)  # Free-text field
    street = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citizens_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citizens_updated')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate a unique citizen ID with the prefix 'CIT'
        if not self.citizen_id:
            while True:
                candidate_id = f'{self.PREFIX}{get_random_string(length=6).upper()}'
                if not Citizen.objects.filter(citizen_id=candidate_id).exists():
                    self.citizen_id = candidate_id
                    break
        super(Citizen, self).save(*args, **kwargs)

    def clean(self):
        if self.mobile1 == self.mobile2:
            raise ValidationError('Mobile numbers must be different.')

    def __str__(self):
        return self.citizen_id

class Company(models.Model):
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = str(TABLE_PREFIX) + "company"

    CHOICES = (
        ("BUYER", "Buyer"),
        ("SELLER", "Seller"),
        ("BOTH", "Both"),
    )

    code = models.CharField(max_length=100, editable=False, unique=True)
    type = models.CharField(max_length=6, default=CHOICES[1], choices=CHOICES, blank=False)
    name = models.CharField(max_length=55, unique=True)
    slug = models.SlugField(unique=True)
    email = models.CharField(max_length=55, null=True, blank=True)
    gst_no = models.CharField(max_length=40, null=True, blank=True)
    pan_no = models.CharField(max_length=40, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    contact_name = models.CharField(max_length=55, null=True, blank=True)
    contact_email = models.CharField(max_length=55, null=True, blank=True)
    contact_mobile = models.IntegerField(null=True, blank=True)
    opening_balance = models.DecimalField(max_digits=50, null=True, decimal_places=2)
    image = models.ImageField(upload_to="company", null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)
    address = models.TextField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=60, null=True, blank=True)
    pin_code = models.CharField(max_length=60, null=True, blank=True)
    status = models.BooleanField(verbose_name="active", default=False)
    created_by = CurrentUserField()
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:  # if uid of the instance is blank
            self.code = "ACC" + str(self.id + (10 ** 5))  # generating the uid and allocating the value
            self.save()  # saving the instance

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Customer(models.Model):
    class Meta:
        verbose_name_plural = "Customers"
        db_table = str(TABLE_PREFIX) + "customers"

    code = models.CharField(max_length=100, editable=False, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60, null=True, blank=True)
    email = models.CharField(max_length=60, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True)
    tin_number = models.CharField(max_length=12, null=True, blank=True)
    pan_number = models.CharField(max_length=10, null=True, blank=True)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    opening_balance = models.DecimalField(max_digits=50, null=True, decimal_places=2)
    image = models.ImageField(upload_to="customer", null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)
    address = models.TextField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=60, null=True, blank=True)
    pin_code = models.CharField(max_length=60, null=True, blank=True)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(verbose_name="created date", blank=True)
    modified_at = models.DateTimeField(verbose_name="modified date", blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:  # if uid of the instance is blank
            self.code = "CUS" + str(self.id + (10 ** 5))  # generating the uid and allocating the value
            self.save()  # saving the instance

    def __str__(self):
        return self.first_name


class Customer(models.Model):
    class Meta:
        verbose_name_plural = "Customers"
        db_table = str(TABLE_PREFIX) + "customers"

    code = models.CharField(max_length=100, editable=False, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60, null=True, blank=True)
    email = models.CharField(max_length=60, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True)
    tin_number = models.CharField(max_length=12, null=True, blank=True)
    pan_number = models.CharField(max_length=10, null=True, blank=True)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    opening_balance = models.DecimalField(max_digits=50, null=True, decimal_places=2)
    image = models.ImageField(upload_to="customer", null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)
    address = models.TextField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=60, null=True, blank=True)
    pin_code = models.CharField(max_length=60, null=True, blank=True)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(verbose_name="created date", blank=True)
    modified_at = models.DateTimeField(verbose_name="modified date", blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:  # if uid of the instance is blank
            self.code = "CUS" + str(self.id + (10 ** 5))  # generating the uid and allocating the value
            self.save()  # saving the instance

    def __str__(self):
        return self.first_name


class PaymentTypes(models.Model):
    class Meta:
        verbose_name_plural = "Payment Types"
        db_table = str(TABLE_PREFIX) + "payment_types"

    code = models.CharField(max_length=100, editable=False, unique=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:  # if uid of the instance is blank
            self.code = "PT" + str(self.id + (10 ** 5))  # generating the uid and allocating the value
            self.save()  # saving the instance

    def __str__(self):
        return self.name


class LoanAccounts(models.Model):
    class Meta:
        verbose_name_plural = "Loan Accounts"
        db_table = str(TABLE_PREFIX) + "loan_accounts"

    code = models.CharField(max_length=100, editable=False, unique=True)
    owners_name = models.CharField(max_length=50, blank=False)
    company_name = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=12)
    notes = models.TextField(max_length=400, null=True, blank=True)
    address = models.TextField(max_length=400, null=True, blank=True)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:  # if uid of the instance is blank
            self.code = "LA" + str(self.id + (10 ** 5))  # generating the uid and allocating the value
            self.save()  # saving the instance

    def __str__(self):
        return self.owners_name


class MasterExpenses(models.Model):
    class Meta:
        verbose_name_plural = "Master Expenses"
        db_table = str(TABLE_PREFIX) + "master_expenses"

    code = models.CharField(max_length=100, editable=False, unique=True)
    name = models.CharField(max_length=50, unique=True)
    notes = models.TextField(max_length=400, null=True, blank=True)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:  # if uid of the instance is blank
            self.code = "MEXP" + str(self.id + (10 ** 5))  # generating the uid and allocating the value
            self.save()  # saving the instance

    def __str__(self):
        return self.name


class Debit(models.Model):
    class Meta:
        verbose_name_plural = "Debits"
        db_table = str(TABLE_PREFIX) + "debit"

    code = models.CharField(max_length=100, editable=False, unique=True)
    debit_date = models.DateTimeField(verbose_name="debit date")
    company_mode = models.ForeignKey(Company, related_name='Company', on_delete=models.CASCADE)
    payment_mode = models.ForeignKey(PaymentTypes, related_name='PaymentType', on_delete=models.CASCADE)
    reference_number = models.TextField(max_length=150, null=True, blank=True)
    amount = models.DecimalField(max_digits=50, null=True, decimal_places=2)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:  # if uid of the instance is blank
            self.code = "DBT" + str(self.id + (10 ** 5))  # generating the uid and allocating the value
            self.save()  # saving the instance

    def __str__(self):
        return self.code


class Credit(models.Model):
    class Meta:
        verbose_name_plural = "Credits"
        db_table = str(TABLE_PREFIX) + "credit"

    code = models.CharField(max_length=100, editable=False, unique=True)
    credit_date = models.DateTimeField(verbose_name="credit date")
    company_mode = models.ForeignKey(Company, related_name='companies', on_delete=models.CASCADE)
    payment_mode = models.ForeignKey(PaymentTypes, related_name='pt', on_delete=models.CASCADE)
    reference_number = models.TextField(max_length=150, null=True, blank=True)
    amount = models.DecimalField(max_digits=50, null=True, decimal_places=2)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:  # if uid of the instance is blank
            self.code = "CRD" + str(self.id + (10 ** 5))  # generating the uid and allocating the value
            self.save()  # saving the instance

    def __str__(self):
        return self.code


class Expenses(models.Model):
    class Meta:
        verbose_name_plural = "Expenses"
        db_table = str(TABLE_PREFIX) + "expenses"

    code = models.CharField(max_length=100, editable=False, unique=True)
    expense_date = models.DateTimeField(verbose_name="expense date")
    expense_mode = models.ForeignKey(MasterExpenses, related_name='MasterExpenses', on_delete=models.CASCADE)
    payment_mode = models.ForeignKey(PaymentTypes, related_name='PaymentTypes', on_delete=models.CASCADE)
    notes = models.TextField(max_length=400, null=True, blank=True)
    amount = models.DecimalField(max_digits=50, null=True, decimal_places=2)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:  # if uid of the instance is blank
            self.code = "EXP" + str(self.id + (10 ** 5))  # generating the uid and allocating the value
            self.save()  # saving the instance

    def __str__(self):
        return self.notes


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Product Category"
        db_table = str(TABLE_PREFIX) + "Category"

    code = models.CharField(max_length=100, editable=False, unique=True)
    category_name = models.CharField(max_length=50, unique=True)
    category_description = models.TextField(max_length=400, null=True, blank=True)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:  # if uid of the instance is blank
            self.code = "CAT" + str(self.id + (10 ** 5))  # generating the uid and allocating the value
            self.save()  # saving the instance

    def __str__(self):
        return self.category_name


class UnitOfMeasurement(models.Model):
    class Meta:
        verbose_name_plural = "Unit of Measurement"
        db_table = str(TABLE_PREFIX) + "unit_of_measurement"

    code = models.CharField(max_length=100, editable=False, unique=True)
    unit_name = models.CharField(max_length=50, unique=True)
    unit_type = models.CharField(max_length=50, unique=True)
    unit_description = models.TextField(max_length=400, null=True, blank=True)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:  # if uid of the instance is blank
            self.code = "UOM" + str(self.id + (10 ** 5))  # generating the uid and allocating the value
            self.save()  # saving the instance

    def __str__(self):
        return self.unit_name


class Products(models.Model):
    class Meta:
        verbose_name_plural = "Products"
        db_table = str(TABLE_PREFIX) + "products"

    code = models.CharField(max_length=100, editable=False, unique=True)
    name = models.CharField(max_length=50, unique=True)
    tag = models.SlugField(max_length=50, null=True,  blank=True)
    hsn_code = models.CharField(max_length=50, null=True,  blank=True)
    price = models.DecimalField(max_digits=50, null=True, decimal_places=2)
    min_stock = models.IntegerField(null=True)
    current_stock = models.IntegerField(null=True)
    tax = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    category = models.ForeignKey(Category, related_name='productCategory', on_delete=models.CASCADE)
    unit = models.ForeignKey(UnitOfMeasurement, related_name='ProductUnitOfMeasurement', on_delete=models.CASCADE)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:
            self.code = "PRD" + str(self.id + (10 ** 5))
            self.save()

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    class Meta:
        verbose_name_plural = "PurchaseOrder"
        db_table = str(TABLE_PREFIX) + "purchaseOrder"

    PURCHASE_TYPE = (
        ("WITH_TAX", "With Tax"),
        ("WITHOUT_TAX", "Without Tax")
    )
    TAX_TYPE = (
        ("GST", "GST"),
        ("IGST", "IGST")
    )
    code = models.CharField(max_length=100, editable=False, unique=True)
    seller_id = models.ForeignKey(Company, related_name='category', on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=50, null=True, blank=True)
    invoice_date = created_at = models.DateTimeField(auto_now_add=True, verbose_name="invoice date")
    hsn_code = models.CharField(max_length=50, null=True,  blank=True)
    purchase_type = models.CharField(max_length=50, choices=PURCHASE_TYPE, null=True, blank=True)
    tax_type = models.CharField(max_length=50, choices=TAX_TYPE, null=True, blank=True)
    value = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    discount = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    gst = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    igst = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    final_value = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    is_paid = models.BooleanField(default=True)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:
            self.code = "PO" + str(self.id + (10 ** 5))
            self.save()

    def __str__(self):
        return self.code


class PurchaseOrderItem(models.Model):
    class Meta:
        verbose_name_plural = "PurchaseOrderItem"
        db_table = str(TABLE_PREFIX) + "purchaseOrderItem"

    code = models.CharField(max_length=100, editable=False, unique=True)
    product = models.ForeignKey(Products, on_delete=models.PROTECT, related_name='product_item')
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='order_items')
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    discount_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    final_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    status = models.BooleanField(max_length=50, default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created date")
    modified_at = models.DateTimeField(
        auto_now_add=True, verbose_name="modified date")

    def save(self, *args, **kwargs):
        self.final_price = self.discount_price if self.discount_price > 0 else self.price
        self.total_price = Decimal(self.qty) * Decimal(self.final_price)
        super().save(*args, **kwargs)
        self.order.save()
        super().save(*args, **kwargs)
        if not self.code:
            self.code = "POI" + str(self.id + (10 ** 5))
            self.save()

    def __str__(self):
        return f'{self.product.name}'


# quantity = models.DecimalField(default=0.00, null=True, decimal_places=2)
# price = models.DecimalField(max_digits=50, null=True, decimal_places=2)
# unit = models.ForeignKey(UnitOfMeasurement, related_name='UnitOfMeasurement', on_delete=models.CASCADE)

