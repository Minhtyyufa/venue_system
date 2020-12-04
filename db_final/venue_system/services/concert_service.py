from venue_system.repositories.concert_repo import ConcertRepo
from venue_system.repositories.venue_repo import VenueRepo
from venue_system.repositories.artist_repo import ArtistRepo
from venue_system.repositories.ticket_repo import TicketRepo
from venue_system.repositories.seat_rank_repo import SeatRankRepo
from django.db import transaction
import uuid

class ConcertService():
    def __init__(self):
        self.concert_repo = ConcertRepo()
        self.venue_repo = VenueRepo()
        self.artist_repo = ArtistRepo()
        self.ticket_repo = TicketRepo()
        self.seat_rank_repo = SeatRankRepo()

    @transaction.atomic
    def create_concert(self, concert_data):
        concert_data["concert_id"] = uuid.uuid4()
        concert_data["venue_id"] = self.venue_repo.get_venue_by_id(concert_data["venue_id"])
        concert_data["artist_id"] = self.artist_repo.get_artist_by_id(concert_data["artist_id"])
        concert  = self.concert_repo.create_concert(concert_data)

        tickets = []
        for i in range(1, concert_data["venue_id"].seat_cols + 1):
            for j in range(1, concert_data["venue_id"].seat_rows +1):
                price = self.seat_rank_repo.get_seat_rank_price(concert_data["venue_id"], i, j)
                if not price:
                    price = concert_data["default_price"]
                tickets.append(self.ticket_repo.create_ticket_no_save(uuid.uuid4(), concert, price, i,j ))

        self.ticket_repo.bulk_insert_tickets(tickets)

        return concert