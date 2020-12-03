from venue_system.repositories.venue_repo import VenueRepo
from django.contrib.gis.geos import Point

class VenueService():
    def __init__(self):
        self.venue_repo = VenueRepo()

    def create_venue(self, venue_data):
        venue_data["location"] = Point(venue_data["location"]["lon"], venue_data["location"]["lat"])
        return self.venue_repo.create_venue(venue_data)
