from django.http import HttpResponse
from rest_framework import viewsets
from venue_system.serializers import CustomUserSerializer
from venue_system.models import CustomUser
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from venue_system.helpers.message import Message
from venue_system.helpers.errors import BaseError, InsufficientFieldsException, WrongAccountTypeException
from venue_system.services.customer_service import CustomerService
import pprint
import json

class CustomerViewSet(viewsets.ModelViewSet):
    customer_service = CustomerService()

    queryset = CustomUser.objects.filter(role_num = 2).order_by("user")
    serializer_class = CustomUserSerializer
    @action(detail = False, url_path = "create_customer", url_name = "create_customer", methods= ["post"])
    def create_customer(self, request):
        message = Message()
        try:

            user_data = request.data
            serializer_context = {
                'request': request,
            }
            pprint.pprint(user_data)
            if user_data.keys() < {"username", "password", "role_num"}:
                raise InsufficientFieldsException("Please provide all of the user fields: username, password, role_num")
            if user_data["role_num"] != 2:
                raise WrongAccountTypeException("Wrong Role number provided for customer: role_num provided" + str(user_data["role_num"]) )

            user = self.customer_service.create_customer(user_data)
            serializer = CustomUserSerializer(user, context = serializer_context)
            print(serializer.data)
            message.add_payload("Successfully created an account", serializer.data)
            return Response(message.response)
        except BaseError as e:
            message.add_error(e)
            return Response(message.response)
