from django.contrib import admin
from .models import Venue, BookVenue

# Register your models here.
admin.site.register(Venue)
admin.site.register(BookVenue)