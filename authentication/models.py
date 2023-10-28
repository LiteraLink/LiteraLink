from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    role = models.CharField(max_length=1)

class UserBook(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    bookID = models.CharField(max_length = 255)
    title = models.CharField(max_length = 255)
    authors = models.CharField(max_length = 255)
    display_authors = models.CharField(max_length = 255)
    description = models.TextField()
    categories = models.CharField(max_length = 255)
    thumbnail = models.TextField()
    feature = models.CharField(max_length=4)




    