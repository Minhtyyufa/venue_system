from django.test import TestCase
import json
from venue_system.models import Artist, User, Venue, CustomUser, Role, Concert, Ticket
import pprint
from venue_system.views.customer_view import CustomerViewSet
from venue_system.repositories.venue_repo import VenueRepo
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
import datetime
import requests
import pytz
from django.core.cache import cache

class ConcertTestCase(APITestCase):
    fixtures = ["roles.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        with open("./venue_system/config.json") as json_file:
            data = json.load(json_file)
            self.client_id = data["client_id"]
            self.client_secret = data["client_secret"]
            self.api_addr = "http://" + data["api_hostname"] + ":" + str(data["api_port"])
        self.add_venue()
        self.add_artist()
        self.add_concert()
        self.create_user()

    def tearDown(self):
        cache.clear()
    def add_venue(self):
        venue_data = {
            "username": "test_venue",
            "password": "pass",
            "role_num": 1,
            "location":
                {"lon": 40.712776,
                 "lat": -74.005974,
                 },
            "venue_name": "The Test Venue",
            "seat_rows": 15,
            "seat_cols": 15,
            "address": "41 Cooper Square New York, NY 10003"
        }
        response = self.client.post("/venue_system/venue/create_venue/", data=venue_data, format="json")

        self.venue_id = response.json()["msg"]["payload"]["venue_id"]["id"]

    def add_artist(self):
        artist_data = {
            "username": "tallah",
            "password": "pass",
            "genre": "prog",
            "band_name": "Tallah",
            "role_num": 3
        }
        response = self.client.post("/venue_system/artist/create_artist/", data=artist_data, format="json")

        self.artist_id = response.json()["msg"]["payload"]["artist_id"]["id"]
    def add_concert(self):
        concert_data = {
            "concert_name": "Tallah (18+)",
            "venue_id": self.venue_id,
            "artist_id": self.artist_id,
            "date_time": datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
            "default_price": 4500
        }

        response = self.client.post("/venue_system/venue/create_concert/", data=concert_data, format="json")
        self.concert_id = response.json()["msg"]["payload"]["concert_id"]

    def create_user(self):
        user_data = {
            "username": "test_customer1",
            "password": "password",
            "role_num": 2
        }
        response = self.client.post("/venue_system/customer/create_customer/", data=user_data, format="json")

        response = self.client.post("/venue_system/api-token-auth/", data= user_data, format="json")
        self.token = response.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.token)
        #pprint.pprint(response.json())

    def test_find_concerts(self):
        query_data = {
            "start_date": datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(days=1)
        }
        response = self.client.get("/venue_system/customer/find_concerts/", query_data)

        self.assertEqual(1, len(response.json()["msg"]["payload"]))

        query_data = {
            "start_date": datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(days=1),
            "artist_id__band_name": "Tall"
        }
        response = self.client.get("/venue_system/customer/find_concerts/", query_data)

        self.assertEqual(1, len(response.json()["msg"]["payload"]))