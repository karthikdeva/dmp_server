
import graphene
from graphene import relay, ObjectType, Connection, Node, Int, String
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model

from .models import Products, PurchaseOrderItem, PurchaseOrder, Category, UnitOfMeasurement,  Customer, PaymentTypes, LoanAccounts, MasterExpenses


class ExtendedConnection(graphene.relay.Connection):
    class Meta:
        abstract = True

    total_count = Int()
    edge_count = Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category


class UnitOfMeasurementNode(DjangoObjectType):
    class Meta:
        model = UnitOfMeasurement


class PurchaseOrderNode(DjangoObjectType):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        filter_fields = {
            'code': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class PurchaseOrderItemNode(DjangoObjectType):
    class Meta:
        model = PurchaseOrderItem
        fields = "__all__"
        filter_fields = {
            'code': ['exact', 'icontains', 'istartswith'],
        }
        # interfaces = (relay.Node,)
        # connection_class = ExtendedConnection

class ProductNode(DjangoObjectType):
    class Meta:
        model = Products
        fields = "__all__"
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"
        filter_fields = {
            'first_name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class MasterExpensesNode(DjangoObjectType):
    class Meta:
        model = MasterExpenses
        fields = "__all__"
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class PaymentTypesNode(DjangoObjectType):
    class Meta:
        model = PaymentTypes
        fields = "__all__"
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class LoanAccountsNode(DjangoObjectType):
    class Meta:
        model = LoanAccounts
        fields = "__all__"
        # filterset_class = CustomFilter
        # ['exact', 'icontains', 'istartswith'],
        filter_fields = {
            'owners_name': ['icontains'],
            'company_name': ['icontains'],
            'bank_name': ['icontains'],
            'phone_number': ['icontains']
        }
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
