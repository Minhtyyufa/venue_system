from rest_framework import serializers

from .models import Role, Venue, Artist, CustomUser, Concert, Ticket, SeatRank

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ("role", "role_num")

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("user", "role_num")

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = ("genre", "band_name")

class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venue
        fields = ("venue_id", "seat_rows", "seat_cols", "venue_name", "address", "location")

class ConcertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Concert
        fields = ("concert_id", "concert_name", "venue_id", "artist_id", "date_time")

class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = ("ticket_id", "concert_id", "customer_id", "price", "seat_row", "seat_col")

class SeatRankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SeatRank
        fields = ("seat_rank_id", "venue_id", "seat_rank", "row", "col", "price")