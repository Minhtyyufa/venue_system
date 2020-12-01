from rest_framework import serializers

from .models import Role, Venue

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ("role", "role_num")

class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venue
        fields = ("venue_id", "seat_rows", "seat_cols", "venue_name", "address", "location")
