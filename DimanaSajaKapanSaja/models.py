from django.db import models
from django.contrib.auth.models import User

class Station(models.Model):
    name = models.CharField(max_length = 255)
    address = models.TextField()
    opening_hours = models.CharField(max_length = 50)
    rentable = models.PositiveIntegerField()
    returnable = models.PositiveIntegerField()
    map_location = models.ImageField(upload_to='images/') 

class StationBook(models.Model):
    station = models.ForeignKey(Station, on_delete = models.CASCADE)
    bookID = models.CharField(max_length = 255)
    title = models.CharField(max_length = 255)
    authors = models.CharField(max_length = 255)
    display_authors = models.CharField(max_length = 255)
    description = models.TextField()
    categories = models.CharField(max_length = 255)
    thumbnail = models.TextField()
