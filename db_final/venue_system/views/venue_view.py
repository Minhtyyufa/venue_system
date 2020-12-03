from django.http import HttpResponse
from rest_framework import viewsets
from venue_system.serializers import VenueSerializer
from venue_system.models import Venue
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from venue_system.helpers.message import Message
from venue_system.helpers.errors import BaseError, InsufficientFieldsException, WrongAccountTypeException
from venue_system.services.venue_service import VenueService
import pprint
import json

class VenueViewSet(viewsets.ModelViewSet):
    venue_service = VenueService()

    queryset = Venue.objects.all().order_by("venue_id")
    serializer_class = VenueSerializer
    @action(detail = False, url_path = "create_venue", url_name = "create_venue", methods= ["post"])
    def create_venue(self, request):
        message = Message()
        try:

            user_data = request.data
            serializer_context = {
                'request': request,
            }
            pprint.pprint(user_data)
            if user_data.keys() < {"username", "password", "role_num", "seat_rows", "seat_cols", "venue_name", "address", "location"}:
                raise InsufficientFieldsException("Please provide all of the user fields: username, password, role_num, seat_rows, seat_cols, venue_name, address, location")
            if user_data["role_num"] != 3:
                raise WrongAccountTypeException("Wrong Role number provided for customer: role_num provided" + str(user_data["role_num"]) )

            user = self.venue_service.create_venue(user_data)
            serializer = VenueSerializer(user, context = serializer_context)

            message.add_payload("Successfully created a venue account", serializer.data)
            return Response(message.response)
        except BaseError as e:
            message.add_error(e)
            return Response(message.response)