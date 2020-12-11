from venue_system.models import CustomUser, User, Role
from venue_system.helpers.errors import DatabaseError

class CustomerRepo():
    def __init__(self):
        pass
    def create_customer(self, customer_data):
        try:
            user = User.objects.create_user(username=customer_data["username"],password=customer_data["password"])

            user.save()

            role_num = Role.objects.get(role_num=customer_data["role_num"])
            cust_user = CustomUser(role_num=role_num, user=user)
            cust_user.save()

            return cust_user
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in customer_repo")
