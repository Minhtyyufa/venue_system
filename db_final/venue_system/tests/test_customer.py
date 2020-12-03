from django.test import TestCase
import json
from venue_system.models import Artist, User, Venue, CustomUser, Role, Concert, Ticket
import pprint
from venue_system.views.customer_view import CustomerViewSet
from rest_framework.test import APIRequestFactory, APITestCase, APIClient


class CustomerTestCase(APITestCase):
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
        response = self.client.post("/venue_system/customer/create_customer/", data=user_details, format="json")

        self.assertEqual(
            {
                'err_msg': 'Please provide all of the user fields: username, password, role_num',
                'err_type': 'InsufficientFieldsException'
            }
            , response.json()["err"])

        user_data = {
            "username": "test_customer",
            "password": "pass",
            "role_num": 2
        }
        response = self.client.post("/venue_system/customer/create_customer/", data=user_data, format="json")

        self.assertEqual(
            {'err': {},
             'msg': {'message': 'Successfully created an account',
                     'payload': {'id': 1,
                                 'role_num': {'role': 'customer', 'role_num': 2},
                                 'user': {'username': 'test_customer'}}}}
            ,
            response.json())
