# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, viewsets
# from rest_framework.permissions import IsAuthenticated
# from django.core.paginator import Paginator

# from app.accounts.api.serializers import CustomerSerializer
# from app.accounts.models import Customer


# class CustomerList(APIView):

#     def get(self, request, format=None):
#         customersList = Customer.objects.all().order_by('-joined_on')
#         serializer = CustomerSerializer(customersList, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CustomerSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             data['success'] = 'Saved Success fully'
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

