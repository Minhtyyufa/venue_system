from django.test import TestCase
import requests
from .populate_database import add_venue, add_artist, add_concert, populate_database
import json
from .models import Artist, User, Venue, CustomUser, Role, Concert
from django.contrib.auth.models import User
import pprint
# Create your tests here.
class PopulateTestCase(TestCase):
    fixtures = ["roles.json"]
    def setUp(self):
        with open("./venue_system/bleh.json") as json_file:
            data = json.load(json_file)
            self.client_id = data["client_id"]
            self.client_secret = data["client_secret"]

    def test_venue_added(self):
        r = requests.get(
            'https://api.seatgeek.com/2/venues/595',
            auth=(self.client_id, self.client_secret))

        add_venue(r.json()).save()

        venue = Venue.objects.get(venue_name = "Birchmere Music Hall")
        self.assertEqual(venue.venue_id.user.username, "birchmere-music-hall" )
        self.assertEqual(venue.address, "3701 Mt. Vernon Avenue Alexandria, VA 22305")

    def test_artist_added(self):

        r = requests.get("https://api.seatgeek.com/2/performers/6296",
                         auth = (self.client_id, self.client_secret))

        add_artist(r.json()).save()

        artist = Artist.objects.get(band_name = "The Strokes")
        self.assertEqual(artist.genre, "Rock")
        self.assertEqual(artist.artist_id.user.username, "the-strokes")

    def test_concert_added(self):
        r = requests.get("https://api.seatgeek.com/2/events/5156873",
                         auth=(self.client_id, self.client_secret))
        concert_data = r.json()
        artist = add_artist(concert_data["performers"][0])
        venue = add_venue(concert_data["venue"])
        concert = add_concert(concert_data, artist, venue)

        artist.save()
        venue.save()
        concert.save()
        concert = Concert.objects.get( concert_name= "Car Seat Headrest with Twin Peaks (18+)")
        self.assertEqual(concert.artist_id, artist)
        self.assertEqual(concert.venue_id, venue)

    def test_bulk_inserts(self):
        populate_database(limit = 2200)
        concert = Concert.objects.filter().first()
        print(concert.artist_id.band_name)

