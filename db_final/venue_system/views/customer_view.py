from django.http import HttpResponse
from rest_framework import viewsets
from venue_system.serializers import CustomUserSerializer, TicketSerializer, ConcertSerializer
from venue_system.models import CustomUser, Ticket
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from venue_system.helpers.message import Message
from venue_system.helpers.errors import BaseError, InsufficientFieldsException, WrongAccountTypeException
from venue_system.services.customer_service import CustomerService
from venue_system.services.concert_service import ConcertService
import pprint
import json

class CustomerViewSet(viewsets.ModelViewSet):
    customer_service = CustomerService()
    concert_service = ConcertService()

    queryset = CustomUser.objects.filter(role_num = 2).order_by("user")
    serializer_class = CustomUserSerializer
    # queryset = Ticket.objects.all().filter()
    # serializer_class = TicketSerializer
    @action(detail = False, url_path = "create_customer", url_name = "create_customer", methods= ["post"])
    def create_customer(self, request):
        message = Message()
        try:

            user_data = request.data
            serializer_context = {
                'request': request,
            }

            if user_data.keys() < {"username", "password", "role_num"}:
                raise InsufficientFieldsException("Please provide all of the user fields: username, password, role_num")
            if user_data["role_num"] != 2:
                raise WrongAccountTypeException("Wrong Role number provided for customer: role_num provided" + str(user_data["role_num"]) )

            user = self.customer_service.create_customer(user_data)
            serializer = CustomUserSerializer(user, context = serializer_context)

            message.add_payload("Successfully created an account", serializer.data)
            return Response(message.response)
        except BaseError as e:
            message.add_error(e)
            return Response(message.response)

    @action(detail = False, url_path = "reserve_ticket", url_name = "reserve_ticket", methods= ["post"])
    def reserve_ticket(self, request):
        message = Message()
        try:
            ticket_data = request.data
            if ticket_data.keys() < {"ticket_id"}:
                raise InsufficientFieldsException("Please provide the ticket_id")

            ticket = self.customer_service.reserve_ticket(request.user, ticket_data["ticket_id"])

            serializer = TicketSerializer(ticket)

            message.add_payload("Successfully reserved ticket", serializer.data)
            return Response(message.response)
        except BaseError as e:
            message.add_error(e)
            return Response(message.response)

    @action(detail = False, url_path = "confirm_ticket", url_name = "confirm_ticket", methods= ["post"])
    def confirm_ticket(self, request):
        message = Message()
        try:
            '''
            {
                "credit_card": {
                    "new": Bool,
                    credit card fields,
                    "credit_card_id"
                },
                "ticket_id"
            }
            '''

            if request.data.keys() < {"credit_card", "ticket_id"}:
                raise InsufficientFieldsException("Please provide credit card details and ticket_id")

            credit_card_details = request.data["credit_card"]
            ticket_id = request.data["ticket_id"]
            if credit_card_details["new"] and credit_card_details.keys() < {"credit_card_number", "security_code", "expiration_date", "card_nickname"}:
                raise InsufficientFieldsException("Please provide all of the credit card details: credit_card_number, security_code, expiration_date, card_nickname")
            if not credit_card_details["new"] and credit_card_details.keys() < {"credit_card_id"}:
                raise InsufficientFieldsException("No credit_card_id provided")

            ticket = self.customer_service.confirm_ticket(request.user, ticket_id, credit_card_details)

            serializer = TicketSerializer(ticket)

            message.add_payload("Successfully confirmed ticket", serializer.data)
            return Response(message.response)
        except BaseError as e:
            message.add_error(e)
            return Response(message.response)

    @action(detail = False, url_path = "get_tickets_by_concert_id", url_name = "get_tickets_by_concert_id", methods= ["get"])
    def get_tickets_by_concert_id(self, request):
        message = Message()
        try:
            if request.query_params.keys() < {"concert_id"}:
                raise InsufficientFieldsException("Please provide a concert_id provided")

            concert_id = request.query_params["concert_id"]
            tickets = self.customer_service.get_tickets_by_concert_id(concert_id)

            serializer = TicketSerializer(tickets, many=True)

            message.add_payload("Successfully retrieved ticket", serializer.data)

            return Response(message.response)

        except BaseError as e:
            message.add_error(e)
            return Response(message.response)

    @action(detail = False, url_path = "find_concerts", url_name = "find_concerts", methods= ["get"])
    def find_concerts(self, request):
        message = Message()
        try:
            if request.query_params.keys() < {"start_date"}:
                raise InsufficientFieldsException("Please provide a start_date provided")

            concerts = self.concert_service.find_concerts(request.query_params)
            serializer = ConcertSerializer(concerts, many=True)

            message.add_payload("Successfully retrieved concerts", serializer.data)
            return Response(message.response)
        except BaseError as e:
            message.add_error(e)
            return Response(message.response)