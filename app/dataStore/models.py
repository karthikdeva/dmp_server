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


class Citizen(models.Model):
    PREFIX = 'CIT'
    readonly_fields = ('citizen_id',)
    # Custom model field for the unique citizen ID with a prefix
    citizen_id = models.CharField(max_length=20, unique=True, db_index=True)
    #validators=[validators.MinLengthValidator(limit_value=1, message='Name must be at least 25 characters long.')]
    #validators=[validators.RegexValidator(r'^\d{10}$', message='Mobile number must be exactly 10 digits.')]
    name = models.CharField(max_length=255)
    mobile1 = models.CharField(max_length=10)
    mobile2 = models.CharField(max_length=10)
    doorNumber = models.CharField(max_length=50)
    nameOnNamePlate = models.CharField(max_length=255)
    AadhaarNumber = models.CharField(max_length=12, validators=[validators.RegexValidator(r'^\d{12}$', message='Adhar number must be 12 digits.')])
    geoLocation = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    noOneAtHome = models.BooleanField(verbose_name="No one at home", default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citizens_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citizens_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate a unique citizen ID with the prefix 'CIT'
        last_citizen = Citizen.objects.order_by('-citizen_id').first()
        if last_citizen:
            last_numeric_part = int(last_citizen.citizen_id.split('-')[-1])
        else:
            last_numeric_part = 0
        new_numeric_part = last_numeric_part + 1

        # Create the full citizen_id with the "CODE-" prefix
        self.citizen_id = f"CODE-{new_numeric_part:04d}"
        super(Citizen, self).save(*args, **kwargs)

    def clean(self):
        if self.mobile1 == self.mobile2:
            raise ValidationError('Mobile numbers must be different.')

    def __str__(self):
        return self.citizen_id
