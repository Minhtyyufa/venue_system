from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets
from venue_system.serializers import RoleSerializer
from venue_system.models import Role
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from venue_system.populate_database import populate_database
from venue_system.helpers.message import Message
from venue_system.helpers.errors import TestException, BaseError


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by("role")
    serializer_class = RoleSerializer

    @action(detail=False, url_path = "list_roles", url_name="list_roles")
    def list_roles(self, request):

        message = Message()
        try:
            print(request)
            queryset = Role.objects.all().order_by("role")
            serializer = RoleSerializer(queryset, many =True)
            raise TestException("This is a test Exception")
            message.add_payload("Successfully retrieved roles", serializer.data)

            return Response(message.response)
        except BaseError as e:
            message.add_error(e)
            return Response(message.response)



class AdminViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by("role")
    serializer_class = RoleSerializer

    @action(detail=False, url_path="populate_database", url_name="populate_database")
    def populate_database(self, request):
        populate_database()
        return(Response("Done"))

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

