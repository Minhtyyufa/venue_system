from rest_framework import viewsets
from venue_system.serializers import ArtistSerializer
from venue_system.models import Artist
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from venue_system.helpers.message import Message
from venue_system.helpers.errors import BaseError, InsufficientFieldsException, WrongAccountTypeException, FieldTypeException
from venue_system.services.artist_service import ArtistService
import pprint
import json
from rest_framework import status



class ArtistViewSet(viewsets.ModelViewSet):
    artist_service = ArtistService()

    queryset = Artist.objects.all().order_by("artist_id")
    serializer_class = ArtistSerializer

    @action(detail = False, url_path = "create_artist", url_name = "create_artist", methods= ["post"])
    def create_artist(self, request):
        message = Message()
        try:
            artist_data = request.data

            if artist_data.keys() < {"username", "password", "genre", "band_name", "role_num"}:
                raise InsufficientFieldsException("Please provide all of the artist fields: username, password, genre, band_name, and role_num")
            if artist_data["role_num"] != 3:
                raise WrongAccountTypeException("Wrong Role number provided for artist: role_num provided " + str(artist_data["role_num"]))

            artist = self.artist_service.create_artist(artist_data)
            serializer = ArtistSerializer(artist)

            message.add_payload("Successfully created an artist account", serializer.data)
            return Response(message.response)
        except BaseError as e:
            message.add_error(e)
            return Response(message.response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path="get_artist_by_id", url_name="get_artist_by_id", methods=["get"])
    def get_artist_by_id(self, request):
        message = Message()

        try:
            if "artist_id" not in request.query_params:
                InsufficientFieldsException("Please provide a artist_id")
            try:
                artist_id = int(request.query_params["artist_id"])
            except ValueError:
                raise FieldTypeException("artist_id must be an int")

            artist = self.artist_service.get_artist_by_id(artist_id)
            serializer = ArtistSerializer(artist)
            message.add_payload("Successfully retrieved artist", serializer.data)
            return Response(message.response)

        except BaseError as e:
            message.add_error(e)
            return Response(message.response, status=status.HTTP_400_BAD_REQUEST)
