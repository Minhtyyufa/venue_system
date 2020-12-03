from django.test import TestCase
import json
from venue_system.models import Artist, User, Venue, CustomUser, Role, Concert, Ticket
import pprint
from venue_system.views.customer_view import CustomerViewSet
from rest_framework.test import APIRequestFactory, APITestCase, APIClient


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
                { "lon": 40.712776,
                  "lat": -74.005974,
                  },
            "venue_name": "The Test Venue",
            "seat_rows": 15,
            "seat_cols": 15,
            "address": "41 Cooper Square New York, NY 10003"
        }



        response = self.client.post("/venue_system/venue/create_venue/", data=user_data, format="json")

        self.assertEqual(
            {'err': {},
             'msg': {'message': 'Successfully created a venue account',
                     'payload': {'address': '41 Cooper Square New York, NY 10003',
                                 'location': 'SRID=4326;POINT (40.712776 '
                                             '-74.00597399999999)',
                                 'seat_cols': 15,
                                 'seat_rows': 15,
                                 'venue_id': {'id': 1,
                                              'role_num': {'role': 'venue owner',
                                                           'role_num': 1},
                                              'user': {'username': 'test_venue'}},
                                 'venue_name': 'The Test Venue'}}},
            response.json())
