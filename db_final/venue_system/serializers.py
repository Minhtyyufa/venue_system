from rest_framework import serializers

from .models import Role, Venue, Artist, CustomUser, Concert, Ticket, SeatRank
from django.contrib.auth.models import User

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("role", "role_num")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = CustomUser
        fields = '__all__'
        depth = 1

class ArtistSerializer(serializers.ModelSerializer):
    artist_id = CustomUserSerializer()
    class Meta:
        model = Artist
        fields = "__all__"
        depth = 2
class VenueSerializer(serializers.ModelSerializer):
    venue_id = CustomUserSerializer()
    class Meta:
        model = Venue
        fields = "__all__"
        depth = 2

class ConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ("concert_id", "concert_name", "venue_id", "artist_id", "date_time")

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("ticket_id", "concert_id", "customer_id", "price", "seat_row", "seat_col")

class SeatRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatRank
        fields = ("seat_rank_id", "venue_id", "seat_rank", "row", "col", "price")