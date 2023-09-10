from django.contrib.auth import login
from django.db.models.query import QuerySet
from django.views.generic.base import View
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
import datetime, json
from django.utils.timezone import utc

from .serializers import UserSerializer, RegisterSerializer
from rest_framework.views import APIView

# class TokenCreateView():
  
 

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        # token['last_login'] = user.last_login
        token['status'] = user.is_active
        token['email'] = user.email
        return token

   
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenObtainView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            # update the created time of the token to keep it valid
            token.created = datetime.datetime.utcnow()
            token.save()
        custom_response = {
            'token': token.key,
            'expires_in':token.created,
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'last_login':user.last_login,
            'status':user.is_active,
            'email': user.email
        }
        return Response(custom_response)


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class CitizenView(APIView):

    def get_object(self):
       # try:
        # return Accounts.objects.all()
        # except Accounts.DoesNotExist
        raise status.HTTP_404_NOT_FOUND


    def get(self, request):
        # try:
        queryset = self.get_object()
        serializer = UserSerializer(queryset, many=True)
       # print('Hit by API')
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        try: 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


    