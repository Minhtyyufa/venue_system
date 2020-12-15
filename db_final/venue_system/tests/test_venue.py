from django.test import TestCase
import json
from venue_system.models import Artist, User, Venue, CustomUser, Role, Concert, Ticket
import pprint
from venue_system.views.customer_view import CustomerViewSet
from venue_system.repositories.venue_repo import VenueRepo
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
import datetime


class VenueTestCase(APITestCase):
    fixtures = ["roles.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        with open("./venue_system/config.json") as json_file:
            data = json.load(json_file)
            self.client_id = data["client_id"]
            self.client_secret = data["client_secret"]
            self.api_addr = "http://" + data["api_hostname"] + ":" + str(data["api_port"])

    def test_create_user(self):
        user_details = {}
        response = self.client.post("/venue_system/venue/create_venue/", data=user_details, format="json")

        self.assertEqual(
            {
                'err_msg': 'Please provide all of the user fields: username, password, role_num, seat_rows, seat_cols, venue_name, address, location',
                'err_type': 'InsufficientFieldsException'
            }
            , response.json()["err"])

        user_data = {
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

        response = self.client.post("/venue_system/venue/create_venue/", data=user_data, format="json")

        self.assertEqual(
            {'message': 'Successfully created a venue account',
             'payload': {'address': '41 Cooper Square New York, NY 10003',
                         'location': 'SRID=4326;POINT (40.712776 '
                                     '-74.00597399999999)',
                         'seat_cols': 15,
                         'seat_rows': 15,
                         'venue_id': {'id': 3},
                         'venue_name': 'The Test Venue'}},
            response.json()["msg"])

    def test_venue_by_id(self):
        user_data = {
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

        response = self.client.post("/venue_system/venue/create_venue/", data=user_data, format="json")

        valid_venue_id = response.json()["msg"]["payload"]["venue_id"]["id"]
        invalid_venue_id = 32
        response = self.client.get("/venue_system/venue/get_venue_by_id/", {"venue_id": invalid_venue_id})
        self.assertEqual({'err': {'err_msg': 'DoesNotExist: in venue_repo', 'err_type': 'DatabaseError'},
                          'msg': {}}, response.json())

        response = self.client.get("/venue_system/venue/get_venue_by_id/", {"venue_id": valid_venue_id})

        self.assertEqual(
            {'message': 'Successfully retrieved venue',
             'payload': {'address': '41 Cooper Square New York, NY 10003',
                         'location': 'SRID=4326;POINT (40.712776 '
                                     '-74.00597399999999)',
                         'seat_cols': 15,
                         'seat_rows': 15,
                         'venue_id': {'id': 4},
                         'venue_name': 'The Test Venue'}},
            response.json()["msg"]
        )

    def test_add_concert(self):
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

        venue_id = response.json()["msg"]["payload"]["venue_id"]["id"]

        artist_data = {
            "username": "tallah",
            "password": "pass",
            "genre": "prog",
            "band_name": "Tallah",
            "role_num": 3
        }
        response = self.client.post("/venue_system/artist/create_artist/", data=artist_data, format="json")

        artist_id = response.json()["msg"]["payload"]["artist_id"]["id"]

        concert_data = {
            "concert_name": "Tallah (18+)",
            "venue_id": venue_id,
            "artist_id": artist_id,
            "date_time": datetime.datetime.now(),
            "default_price": 4500
        }

        response = self.client.post("/venue_system/venue/create_concert/", data=concert_data, format="json")

        self.assertEqual({'message': 'Successfully created a concert',
                          'payload': {'artist_id': {'artist_id': {'id': 2},
                                                    'band_name': 'Tallah',
                                                    'genre': 'prog'},
                                      'concert_id': '3bdf82c0-7ad2-486a-a5b5-891b4b33cbdd',
                                      'concert_name': 'Tallah (18+)',
                                      'date_time': '2020-12-03T23:17:09.935616',
                                      'venue_id': {'address': '41 Cooper Square New York, NY '
                                                              '10003',
                                                   'location': 'SRID=4326;POINT (40.712776 '
                                                               '-74.00597399999999)',
                                                   'seat_cols': 15,
                                                   'seat_rows': 15,
                                                   'venue_id': {'id': 1},
                                                   'venue_name': 'The Test Venue'}}}
                         ,
                         response.json()["msg"])
