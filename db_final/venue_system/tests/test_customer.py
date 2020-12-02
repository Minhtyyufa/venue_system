from django.test import TestCase
import requests
import json
from venue_system.models import Artist, User, Venue, CustomUser, Role, Concert, Ticket
import pprint


class CustomerTestCase(TestCase):
    fixtures = ["roles.json"]
    def setUp(self):
        with open("./venue_system/config.json") as json_file:
            data = json.load(json_file)
            self.client_id = data["client_id"]
            self.client_secret = data["client_secret"]
            self.api_addr = "http://" + data["api_hostname"]+ ":" + str(data["api_port"])

    def test_create_user(self):
        user_details = {}
        r = requests.post(self.api_addr + "/venue_system/customer/create_customer/", data=user_details)

        self.assertEqual(
            {
                'err_msg': 'Please provide all of the user fields: username, password, role_num',
                'err_type': 'InsufficientFields'
            }
            , r.json()["err"])