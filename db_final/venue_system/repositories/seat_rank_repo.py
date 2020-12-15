from venue_system.models import SeatRank
from venue_system.helpers.errors import DatabaseError

class SeatRankRepo():
    def __init__(self):
        pass

    def get_seat_rank_price(self, venue_id, col, row):
        try:
            seat_rank = SeatRank.objects.filter(venue_id= venue_id, row= row, col = col).first()
            if seat_rank:
                return seat_rank.price
            else:
                return None
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in seat_rank_repo")
