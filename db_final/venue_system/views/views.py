from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from venue_system.serializers import RoleSerializer, UserSerializer, CustomUserSerializer, TicketSerializer
from venue_system.models import Role, CustomUser, Ticket
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from venue_system.populate_database import populate_database
from venue_system.helpers.message import Message
from venue_system.helpers.errors import TestException, BaseError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by("role")
    serializer_class = RoleSerializer
    permission_classes = (IsAuthenticated,)
    @action(detail=False, url_path = "list_roles", url_name="list_roles")
    def list_roles(self, request):

        message = Message()
        try:
            user = request.user
            print(user.password)
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

