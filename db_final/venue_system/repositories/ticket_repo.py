from venue_system.models import Ticket
from venue_system.helpers.errors import DatabaseError

class TicketRepo():
    def __init__(self):
        pass
    def create_ticket_no_save(self, ticket_id, concert, price, seat_col, seat_row ):
        try:
            return Ticket(ticket_id = ticket_id, concert_id = concert, customer_id = None, price = price,
                          seat_col = seat_col, seat_row = seat_row)
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in ticket_repo")

    def get_ticket_by_id(self, ticket_id):
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            return ticket
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in ticket_repo")
    def bulk_insert_tickets(self, tickets):
        try:
            Ticket.objects.bulk_create(tickets)
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in ticket_repo")

    def save(self, ticket):
        try:
            ticket.save()
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in ticket_repo")

    def get_tickets_by_concert_id(self, concert_id):
        try:
            return Ticket.objects.all().filter(concert_id=concert_id)
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in ticket_repo")

