from rest_framework import serializers
from django.contrib.auth.models import User
# from app.accounts.models import Customer


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email')


# class CustomerSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#
#     class Meta:
#         model = Customer
#         fields = [
#             'id',
#             'user',
#             'phone_number',
#             'birth_date',
#             'image',
#             'joined_on'
#         ]






