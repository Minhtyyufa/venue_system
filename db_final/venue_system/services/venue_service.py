from venue_system.repositories.venue_repo import VenueRepo

class VenueService():
    def __init__(self):
        self.venue_repo = VenueRepo()

    def create_venue(self, venue_data):
        return self.venue_repo.create_venue(venue_data)
