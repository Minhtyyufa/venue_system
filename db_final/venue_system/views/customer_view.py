from django.http import HttpResponse
from rest_framework import viewsets
from venue_system.serializers import CustomUserSerializer
from venue_system.models import CustomUser
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from venue_system.helpers.message import Message
from venue_system.helpers.errors import BaseError, InsufficientFields


class CustomerViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.filter(role_num = 2).order_by("user")
    serializer_class = CustomUserSerializer
    @action(detail = False, url_path = "create_customer", url_name = "create_customer", methods= ["post"])
    def create_customer(self, request):
        message = Message()
        try:
            user_data = request.data
            if user_data.keys() < {"username", "password", "role_num"}:
                raise InsufficientFields("Please provide all of the user fields: username, password, role_num")
            if user_data["role_num"] != 2:
                raise WrongAccountTypeException()


            return Response("bleh")
        except BaseError as e:
            message.add_error(e)
            return Response(message.response)
