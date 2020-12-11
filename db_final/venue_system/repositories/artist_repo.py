from venue_system.models import CustomUser, User, Role, Artist
from venue_system.helpers.errors import DatabaseError

class ArtistRepo():
    def __init__(self):
        pass
    def create_artist(self, artist_data):
        try:
            user = User.objects.create_user(username=artist_data["username"], password=artist_data["password"])
            user.save()

            role_num = Role.objects.get(role_num=artist_data["role_num"])
            cust_user = CustomUser(role_num=role_num, user=user)
            cust_user.save()

            artist = Artist(artist_id=cust_user, genre = artist_data["genre"], band_name = artist_data["band_name"])
            artist.save()
            return artist
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in artist_repo")


    def get_artist_by_id(self, artist_id):
        try:
            artist = Artist.objects.get(artist_id=artist_id)
            return artist
        except Exception as e:
            raise DatabaseError(e.__class__.__name__ + ": in artist_repo")
