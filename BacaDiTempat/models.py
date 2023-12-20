from django.db import models
from authentication.models import UserProfile

# Create your models here.

class Venue(models.Model):
    person_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    book_name = models.CharField(max_length=255)
    place_name = models.CharField(max_length=255)
    map_location = models.ImageField(upload_to='images/') 
    price = models.CharField(max_length=255)
    address = models.TextField()
    venue_open = models.CharField(max_length = 50)
    rent_book = models.PositiveIntegerField()
    return_book = models.PositiveIntegerField()
    date_use = models.DateField(null=True, blank=True)
    date_return = models.DateTimeField(null=True, blank=True)


class BookVenue(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    bookID = models.CharField(max_length = 255)
    title = models.CharField(max_length = 255)
    authors = models.CharField(max_length = 255)
    display_authors = models.CharField(max_length = 255)
    description = models.TextField()
    categories = models.CharField(max_length = 255)
    thumbnail = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, default=None)

