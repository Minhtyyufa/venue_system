from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from venue_system.serializers import RoleSerializer, UserSerializer, CustomUserSerializer, TicketSerializer
from venue_system.models import Role, CustomUser, Ticket
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from venue_system.populate_database import populate_database, add_tickets_to_concerts
from venue_system.helpers.message import Message
from venue_system.helpers.errors import TestException, BaseError
from django.contrib.auth.models import User
from rest_framework import status
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


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by("role")
    serializer_class = RoleSerializer

    @action(detail=False, url_path="populate_database", url_name="populate_database")
    def populate_database(self, request):
        populate_database()
        return(Response("Done"))
    @action(detail=False, url_path="add_tickets_to_concerts", url_name="add_tickets_to_concerts")
    def add_tickets_to_concerts(self, request):
        print(len(Ticket.objects.all()))
        # add_tickets_to_concerts()
        return(Response("Done"))

    @action(detail=False, url_path="get_user_type", url_name="get_user_type")
    def get_user_type(self, request):
        message = Message()
        try:
            message.add_payload("Successfully Retrieved Role", request.user.customuser.role_num.role_num)

            return Response(message.response)
        except BaseError as e:
            message.add_error(e)
            return Response(message.response, status=status.HTTP_400_BAD_REQUEST)
