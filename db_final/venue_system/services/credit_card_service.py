from venue_system.repositories.credit_card_repo import CreditCardRepo

class CreditCardService():
    def __init__(self):
        self.credit_card_repo = CreditCardRepo()

    def create_credit_card(self, credit_card_details):
        return self.credit_card_repo.create_credit_card(credit_card_details)

    def get_credit_card_by_credit_id(self, credit_card_id):
        return self.credit_card_repo.get_credit_card_by_credit_id(credit_card_id)
