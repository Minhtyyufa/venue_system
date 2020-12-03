from venue_system.repositories.customer_repo import CustomerRepo

class CustomerService():
    def __init__(self):
        self.customer_repo = CustomerRepo()

    def create_customer(self, customer_data):
        return self.customer_repo.create_customer(customer_data)
