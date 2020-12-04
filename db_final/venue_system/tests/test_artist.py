import json
import pprint
from rest_framework.test import APIRequestFactory, APITestCase, APIClient


class ArtistTestCase(APITestCase):
    fixtures = ["roles.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        with open("./venue_system/config.json") as json_file:
            data = json.load(json_file)
            self.client_id = data["client_id"]
            self.client_secret = data["client_secret"]
            self.api_addr = "http://" + data["api_hostname"] + ":" + str(data["api_port"])

    def test_create_artist(self):
        artist_data = {}
        response = self.client.post("/venue_system/artist/create_artist/", data=artist_data, format="json")

        self.assertEqual(
            {
                'err_msg': "Please provide all of the artist fields: username, password, genre, band_name, and role_num",
                'err_type': 'InsufficientFieldsException'
            }
            , response.json()["err"])

        artist_data = {
            "username": "tallah",
            "password": "pass",
            "genre": "prog",
            "band_name": "Tallah",
            "role_num": 3
        }

        response = self.client.post("/venue_system/artist/create_artist/", data=artist_data, format="json")
        self.assertEqual(
            {'msg': {'message': 'Successfully created an artist account', 'payload': {
                'artist_id': {'id': 1},
                'genre': 'prog', 'band_name': 'Tallah'}}, 'err': {}},
            response.json())

    def test_venue_by_id(self):
        artist_data = {
            "username": "tallah",
            "password": "pass",
            "genre": "prog",
            "band_name": "Tallah",
            "role_num": 3
        }

        response = self.client.post("/venue_system/artist/create_artist/", data=artist_data, format="json")

        valid_artist_id = response.json()["msg"]["payload"]["artist_id"]["id"]
        invalid_artist_id = 32
        response = self.client.get("/venue_system/artist/get_artist_by_id/", {"artist_id": invalid_artist_id})
        self.assertEqual({'err': {'err_msg': 'DoesNotExist: in artist_repo', 'err_type': 'DatabaseError'},
                          'msg': {}}, response.json())

        response = self.client.get("/venue_system/artist/get_artist_by_id/", {"artist_id": valid_artist_id})
        self.assertEqual(
            {'err': {},
             'msg': {'message': 'Successfully retrieved artist',
                     'payload': {'artist_id': {'id': 2},
                                 'band_name': 'Tallah',
                                 'genre': 'prog'}}},
        response.json())
