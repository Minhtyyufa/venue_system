from venue_system.models import CustomUser, User, Role, Venue

class VenueRepo():
    def __init__(self):
        pass
    def create_venue(self, venue_data):
        user = User(username=venue_data["username"], password=venue_data["password"])
        user.save()

        role_num = Role.objects.get(role_num=venue_data["role_num"])
        cust_user = CustomUser(role_num=role_num, user=user)
        cust_user.save()

        venue = Venue(venue_name=venue_data["venue_name"], address=venue_data["address"], seat_rows = venue_data["seat_rows"],
                      seat_cols = venue_data["seat_cols"], location = venue_data["location"], venue_id = cust_user)

        return venue
