from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid

class Role(models.Model):
    role = models.CharField(max_length=15)
    role_num = models.IntegerField(primary_key=True)

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_num = models.ForeignKey(Role, on_delete=models.DO_NOTHING)



class Venue(models.Model):
    venue_id = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING, primary_key=True)
    seat_rows = models.PositiveIntegerField()
    seat_cols = models.PositiveIntegerField()

    address = models.CharField(max_length= 75)
    mpoly = models.PointField()

class Concert(models.Model):
    concert_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venue_id = models.ForeignKey(Venue, on_delete=models.DO_NOTHING)
    artist_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField()
    class Meta:
        unique_together = [["artist_id", "date_time"]]

class Ticket(models.Model):
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    concert_id = models.ForeignKey(Concert, on_delete=models.DO_NOTHING)
    customer_id = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING, null=True)
    price = models.PositiveIntegerField()
    seat_row = models.PositiveIntegerField()
    seat_col = models.PositiveIntegerField()
    class Meta:
        unique_together = [["seat_col", "seat_col", "concert_id"]]


class SeatRank(models.Model):
    seat_rank_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    venue_id = models.ForeignKey(Venue, on_delete=models.DO_NOTHING)
    seat_rank = models.CharField(max_length=5)
    row = models.PositiveIntegerField()
    col = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

