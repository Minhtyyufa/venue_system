from django.contrib import admin

from .models import Role, CustomUser, Venue, SeatRank, Concert, Ticket

#admin.site.register(User)
# Register your models here.
admin.site.register([Role, CustomUser, Venue, SeatRank, Concert, Ticket])
