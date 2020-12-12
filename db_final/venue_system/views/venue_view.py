from django.http import HttpResponse
from rest_framework import viewsets
from venue_system.serializers import VenueSerializer, ConcertSerializer
from venue_system.models import Venue
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from venue_system.helpers.message import Message
from venue_system.helpers.errors import BaseError, InsufficientFieldsException, WrongAccountTypeException, FieldTypeException
from venue_system.services.venue_service import VenueService
from venue_system.services.concert_service import ConcertService
import pprint
import json
from rest_framework import status



class VenueViewSet(viewsets.ModelViewSet):
    venue_service = VenueService()
    concert_service = ConcertService()
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
            if user_data.keys() < {"username", "password", "role_num", "seat_rows", "seat_cols", "venue_name", "address", "location"}:
                raise InsufficientFieldsException("Please provide all of the user fields: username, password, role_num, seat_rows, seat_cols, venue_name, address, location")
            if user_data["location"].keys() < {"lon", "lat"}:
                raise InsufficientFieldsException("Please provide all of the location fields: lon, lat")
            if user_data["role_num"] != 1:
                raise WrongAccountTypeException("Wrong Role number provided for customer: role_num provided " + str(user_data["role_num"]) )

            user = self.venue_service.create_venue(user_data)
            serializer = VenueSerializer(user, context = serializer_context)

            message.add_payload("Successfully created a venue account", serializer.data)
            return Response(message.response)
        except BaseError as e:
            message.add_error(e)
            return Response(message.response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path="create_concert", url_name="create_concert", methods=["post"])
    def create_concert(self, request):
        message = Message()
        try:
            concert_data = request.data
            print(request.user.customuser.role_num.role_num)
            if request.user.customuser.role_num.role_num != 1:
                raise WrongAccountTypeException("You're not a venue_owner")
            if concert_data.keys() < {"concert_name", "artist_id", "date_time", "default_price"}:
                raise InsufficientFieldsException("Please provide all of the concert fields: concert_name, venue_id, artist_id, date_time")
            try:
                concert_data["artist_id"] = int(concert_data["artist_id"])
            except ValueError:
                raise FieldTypeException("venue_id must be an int")
            venue = request.user.customuser.venue

            concert_data["venue_id"]=venue
            pprint.pprint(concert_data)
            concert = self.concert_service.create_concert(concert_data)

            serializer=ConcertSerializer(concert)
            message.add_payload("Successfully created a concert", serializer.data)

            return Response(message.response)
        except BaseError as e:
            message.add_error(e)
            return Response(message.response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path="get_venue_by_id", url_name="get_venue_by_id", methods=["get"])
    def get_venue_by_id(self, request):
        message = Message()

        try:
            if "venue_id" not in request.query_params:
                InsufficientFieldsException("Please provide a venue_id")
            try:
                venue_id = int(request.query_params["venue_id"])
            except ValueError:
                raise FieldTypeException("venue_id must be an int")

            venue = self.venue_service.get_venue_by_id(venue_id)
            serializer = VenueSerializer(venue)
            message.add_payload("Successfully retrieved venue", serializer.data)
            return Response(message.response)

        except BaseError as e:
            message.add_error(e)
            return Response(message.response, status=status.HTTP_400_BAD_REQUEST)
