from venue_system.models import CreditCard
from venue_system.helpers.errors import DatabaseError
import uuid
class CreditCardRepo():
    def __init__(self):
        pass
    def create_credit_card(self, credit_card):
        try:
            credit_card = CreditCard(credit_card_id = uuid.uuid4(), credit_card_number=credit_card["credit_card_number"],
                                     security_code = credit_card["security_code"],
                                     expiration_date = credit_card["expiration_date"],
                                     card_nickname = credit_card["card_nickname"],
                                     customer_id = credit_card["customer_id"])
            credit_card.save()
            return credit_card
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in credit_card_repo")

    def get_credit_card_by_credit_id(self, credit_id):
        try:
            credit_card = CreditCard.objects.get(credit_card_id=credit_id)
            return credit_card
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in credit_card_repo")
