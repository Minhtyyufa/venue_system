from rest_framework import serializers
import datetime
import pytz
from .models import Role, Venue, Artist, CustomUser, Concert, Ticket, SeatRank, CreditCard
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
    #user = UserSerializer()
    class Meta:
        model = CustomUser
        fields = ["id"]
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
    artist_id = ArtistSerializer()
    venue_id = VenueSerializer()
    class Meta:
        model = Concert
        fields = ("concert_id", "concert_name", "venue_id", "artist_id", "date_time")
        depth = 2
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

class SeatRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatRank
        fields = ("seat_rank_id", "venue_id", "seat_rank", "row", "col", "price")

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = "__all__"

class AvailableTicketSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField("get_is_available")
    def get_is_available(self, obj):
        return obj.purchased_timestamp == None or (datetime.datetime.utcnow().replace(tzinfo=pytz.utc) >obj.purchased_timestamp and obj.credit_card_id == None)
    class Meta:
        model = Ticket
        fields = ("ticket_id","seat_col", "seat_row", "price", "is_available")