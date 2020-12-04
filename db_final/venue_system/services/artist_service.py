from venue_system.repositories.artist_repo import ArtistRepo
from django.contrib.gis.geos import Point


class ArtistService():
    def __init__(self):
        self.artist_repo = ArtistRepo()

    def create_artist(self, artist_data):
        return self.artist_repo.create_artist(artist_data)

    def get_artist_by_id(self, artist_id):
        return self.artist_repo.get_artist_by_id(artist_id)
    # def create_concert(self, concert_data):
    #     pass
