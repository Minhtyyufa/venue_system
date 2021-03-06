from venue_system.repositories.venue_repo import VenueRepo
from django.contrib.gis.geos import Point
from django.db import transaction

class VenueService():
    def __init__(self):
        self.venue_repo = VenueRepo()

    @transaction.atomic
    def create_venue(self, venue_data):
        venue_data["location"] = Point(venue_data["location"]["lon"], venue_data["location"]["lat"])
        return self.venue_repo.create_venue(venue_data)

    def get_venue_by_id(self, venue_id):
        return self.venue_repo.get_venue_by_id(venue_id)

