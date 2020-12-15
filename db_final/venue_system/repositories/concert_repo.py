from venue_system.models import Concert
from venue_system.helpers.errors import DatabaseError
import pprint

class ConcertRepo():
    def __init__(self):
        pass
    def create_concert(self, concert_data):
        try:
            concert = Concert(concert_id = concert_data["concert_id"], concert_name = concert_data["concert_name"], venue_id = concert_data["venue_id"],
                    artist_id = concert_data["artist_id"], date_time = concert_data["date_time"])
            concert.save()
            return concert
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in concert_repo")

    def find_concerts(self, request_params):
        try:
            concerts = {
                "date_time__gte": request_params["start_date"]
            }

            for k, v in request_params.items():
                # if k == "genre":
                #     concerts["artist_id__genre__contains"] = v
                # elif k == ""
                if k == "start_date":
                    continue
                elif v[0] == "":
                    continue
                elif k == "end_date":
                    concerts["date_time__lte"] = v[0]
                else:
                    concerts[k+"__icontains"] = v[0]
            return Concert.objects.filter(**concerts).order_by("date_time", "concert_name")
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in concert_repo")

    def get_concerts_by_venue(self, venue):
        try:
            return Concert.objects.filter(venue_id = venue).order_by("date_time")
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in concert_repo")