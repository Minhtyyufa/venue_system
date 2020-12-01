import json
import requests
import pprint
from .models import Venue, CustomUser, Role, Artist, Concert
import uuid
from django.contrib.auth.models import User
import numpy as np
from django.contrib.gis.geos import Point
from django.db import transaction
import datetime
import pytz
from dateutil import parser

def add_concert(concert_data, artist, venue):
    concert_id = uuid.uuid4()
    concert_name = concert_data["short_title"]
    date_time = parser.parse(concert_data["datetime_utc"] + " UTC")
    return Concert(concert_id = concert_id, concert_name= concert_name, date_time = date_time, venue_id = venue, artist_id= artist)

def add_artist(artist_data):
    artist_user = User(username = artist_data["slug"], password = "CooperCU2021!!!")
    artist_user.save()

    role_num = Role.objects.get(role="artist")
    cust_user = CustomUser(role_num = role_num, user = artist_user)
    cust_user.save()
    if "genres" not in artist_data:
        genre = ""
    else:
        genre = artist_data["genres"][0]["name"]
    artist = Artist(genre = genre, band_name = artist_data["short_name"], artist_id = cust_user)
    return artist



def add_venue(venue_data):
    venue_user = User(username= venue_data["slug"], password = "CooperCU2021!!!")
    venue_user.save()

    role_num = Role.objects.get(role="venue owner")
    cust_user = CustomUser(role_num=role_num, user=venue_user)
    cust_user.save()

    venue_name = venue_data["name"]

    address = venue_data["address"] if venue_data["address"] is not None else ""

    if "extended_address" in venue_data and venue_data["extended_address"] is not None:
        address += " " + venue_data["extended_address"]
    temp = int(np.sqrt(venue_data["capacity"]))
    seat_rows = temp
    seat_cols = temp
    mpoly = Point(venue_data["location"]["lon"], venue_data["location"]["lat"])
    venue = Venue(venue_name=venue_name, address=address, seat_rows=seat_rows, seat_cols = seat_cols, location = mpoly,
                  venue_id=cust_user)

    return venue



@transaction.atomic
def populate_database(limit = 30000):
    with open("./venue_system/bleh.json") as json_file:
        data = json.load(json_file)
    r = requests.get(
        'https://api.seatgeek.com/2/events?datetime_utc.gt=2012-09-07&type=concert&per_page=1&format=json&venue.country=US',
        auth=(data["client_id"], data["client_secret"]))
    total_events = r.json()["meta"]["total"]

    i = 1
    artists = {}
    venues = {}
    concert_ids = set()
    concert_list = []
    while i*1000 < total_events and i*1000 < limit:
        r = requests.get(
            'https://api.seatgeek.com/2/events?datetime_utc.gt=2012-09-07&type=concert&per_page=1000&format=json&venue.country=US&page=' + str(i),
            auth=(data["client_id"], data["client_secret"]))

        concerts = r.json()["events"]
        for concert in concerts:
            if concert["id"] in concert_ids:
                continue
            if concert["performers"][0]["id"] in artists:
                artist = artists[concert["performers"][0]["id"]]
            else:
                artist = add_artist(concert["performers"][0])
                artists[concert["performers"][0]["id"]] = artist

            if concert["venue"]["id"] in venues:
                venue = venues[concert["venue"]["id"]]
            else:
                venue = add_venue(concert["venue"])
                venues[concert["venue"]["id"]] = venue

            concert_list.append(add_concert(concert, artist, venue))
            concert_ids.add(concert["id"])

        i += 1

    Artist.objects.bulk_create(list(artists.values()))
    Venue.objects.bulk_create(list(venues.values()))
    Concert.objects.bulk_create(list(concert_list))

