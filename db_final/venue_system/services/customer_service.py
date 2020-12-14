from venue_system.repositories.customer_repo import CustomerRepo
from venue_system.repositories.ticket_repo import TicketRepo
from venue_system.repositories.credit_card_repo import CreditCardRepo
from django.db import transaction
from venue_system.helpers.errors import TicketReservedAlreadyError
import datetime
import pytz

class CustomerService():
    def __init__(self):
        self.customer_repo = CustomerRepo()
        self.ticket_repo = TicketRepo()
        self.credit_card_repo = CreditCardRepo()

    @transaction.atomic
    def create_customer(self, customer_data):
        return self.customer_repo.create_customer(customer_data)

    @transaction.atomic
    def reserve_ticket(self, user, ticket_id):

        ticket = self.ticket_repo.get_ticket_by_id(ticket_id)
        if ticket.purchased_timestamp == None or (datetime.datetime.utcnow().replace(tzinfo=pytz.utc) >ticket.purchased_timestamp and ticket.credit_card_id == None):
            ticket.customer_id = user.customuser
            ticket.purchased_timestamp = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)+datetime.timedelta(minutes=5)
            self.ticket_repo.save(ticket)
        else:
            raise TicketReservedAlreadyError("This tickets has been reserved already")
        return ticket

    @transaction.atomic
    def confirm_ticket(self, user, ticket_id, credit_card_details):
        user = user.customuser
        if credit_card_details["new"]:
            credit_card_details["customer_id"]=user
            credit_card = self.credit_card_repo.create_credit_card(credit_card_details)
        else:
            credit_card = self.credit_card_repo.get_credit_card_by_credit_id(credit_card_details["credit_card_id"])
        ticket = self.ticket_repo.get_ticket_by_id(ticket_id)

        if ticket.customer_id == user and ticket.purchased_timestamp > datetime.datetime.utcnow().replace(tzinfo=pytz.utc):
            ticket.purchased_timestamp = datetime.datetime.now()
            ticket.credit_card_id = credit_card
            self.ticket_repo.save(ticket)
        return ticket

    def get_tickets_by_concert_id(self, concert_id):
        return self.ticket_repo.get_tickets_by_concert_id(concert_id)

    def get_my_tickets(self, user):
        return self.ticket_repo.get_tickets_for_user(user)

