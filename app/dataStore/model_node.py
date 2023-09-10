
import graphene
from graphene import relay, ObjectType, Connection, Node, Int, String
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model

from .models import Citizen


class ExtendedConnection(graphene.relay.Connection):
    class Meta:
        abstract = True

    total_count = Int()
    edge_count = Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class CitizenNode(DjangoObjectType):
    class Meta:
        model = Citizen
        fields = "__all__"
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
