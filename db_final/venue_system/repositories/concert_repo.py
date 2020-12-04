from venue_system.models import Concert

class ConcertRepo():
    def __init__(self):
        pass
    def create_concert(self, concert_data):
        concert = Concert(concert_id = concert_data["concert_id"], concert_name = concert_data["concert_name"], venue_id = concert_data["venue_id"],
                artist_id = concert_data["artist_id"], date_time = concert_data["date_time"])
        concert.save()
        return concert